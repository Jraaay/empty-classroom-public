<template>
  <div>
    <el-container>
      <el-col v-loading="loading ?? true">
        <el-row style="place-content: center">
          <img
            src="./assets/logo.png"
            style="width: 7em; margin-top: -2em; margin-bottom: -2em"
          />
        </el-row>
        <el-row style="place-content: center">
          <h1 class="title">BUPT 空教室查询</h1>
        </el-row>
        <div v-if="!apiError">
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-if="notification"
          >
            <el-button @click="showNotification" text bg :icon="Info">{{
              notification?.title
            }}</el-button>
          </el-row>
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-if="hasNewVer"
          >
            <el-button
              @click="showUpdate"
              text
              bg
              :icon="Opportunity"
              type="success"
              >检测到新版本
              <el-tag size="small" type="success" style="margin-left: 5px">{{
                newVer
              }}</el-tag>
            </el-button>
          </el-row>
          <el-row style="place-content: center">
            <el-row
              style="
                place-content: center;
                margin-bottom: 20px;
                width: 90%;
                max-width: 400px;
              "
            >
              <el-button
                @click="report"
                style="padding: 10px; border-radius: 0px; margin-right: 15px"
              >
                <el-icon>
                  <ChatLineSquare />
                </el-icon>
              </el-button>
              <el-radio-group v-model="campus_id">
                <el-radio-button label="西土城" />
                <el-radio-button label="沙河" />
              </el-radio-group>
              <el-button
                @click="dialogVisible = true"
                style="padding: 10px; border-radius: 0px; margin-left: 15px"
              >
                <el-icon>
                  <Setting />
                </el-icon>
              </el-button>
            </el-row>
          </el-row>
          <el-row style="place-content: center; margin-bottom: 20px">
            <el-alert
              :title="'当前查询日期：' + empty_rooms?.time?.split(' ')[0]"
              type="info"
              center
              :closable="false"
              style="width: 90%; max-width: 400px"
            />
          </el-row>
          <el-row style="place-content: center; margin-bottom: 20px">
            <el-row
              style="
                width: 90%;
                max-width: 400px;
                padding-top: 5px;
                padding-bottom: 5px;
                place-content: center;
              "
              class="checkgroupView"
            >
              <el-row
                style="padding: 15px; text-align: center"
                class="pick-building"
              >
                <el-checkbox-group v-model="building">
                  <el-checkbox-button
                    v-for="i in building_all"
                    :key="i"
                    :label="i"
                  >
                    <div style="position: relative; width: fit-content">
                      {{ i }}
                      <div
                        style="position: absolute; right: -8px; top: 0px"
                        v-if="trustBuilding.indexOf(i) == -1"
                      >
                        *
                      </div>
                    </div>
                  </el-checkbox-button>
                </el-checkbox-group>
              </el-row>
              <el-row>
                <el-alert
                  :title="'* : 来自教室课表，可能不准确'"
                  type="info"
                  center
                  :closable="false"
                  style="width: 100%; margin-top: -10px; margin-bottom: 10px"
                />
              </el-row>
            </el-row>
          </el-row>
          <el-row style="place-content: center; margin-bottom: 20px">
            <el-row
              style="
                width: 90%;
                max-width: 400px;
                padding-top: 5px;
                padding-bottom: 5px;
                place-content: center;
              "
              class="checkgroupView"
            >
              <el-row style="width: 280px; padding: 10px">
                <el-checkbox-group v-model="checkboxGroup">
                  <el-checkbox-button
                    v-for="class_id in classes"
                    :key="class_id"
                    :label="class_id"
                    :disabled="
                      !(
                        new Date().getHours() > 20 ||
                        (new Date().getHours() == 20 &&
                          new Date().getMinutes() >= 55)
                      ) &&
                      (new Date().getHours() >
                        parseInt(
                          class_time[parseInt(class_id) - 1].split(':')[0]
                        ) ||
                        (new Date().getHours() ==
                          parseInt(
                            class_time[parseInt(class_id) - 1].split(':')[0]
                          ) &&
                          new Date().getMinutes() >=
                            parseInt(
                              class_time[parseInt(class_id) - 1].split(':')[1]
                            )))
                    "
                  >
                    <div
                      style="font-size: 0.7em; margin-bottom: 2px"
                      v-if="showTime"
                    >
                      {{ class_start_time[parseInt(class_id) - 1] }}
                    </div>
                    {{ class_id }}
                    <div
                      style="font-size: 0.7em; margin-top: 2px"
                      v-if="showTime"
                    >
                      {{ class_time[parseInt(class_id) - 1] }}
                    </div>
                  </el-checkbox-button>
                  <el-button @click="handleCheckAllChange" class="checkAll">{{
                    checkedAll() ? "全不选" : "全选"
                  }}</el-button>
                </el-checkbox-group>
              </el-row>
            </el-row>
          </el-row>
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-if="building.length == 0"
          >
            <el-row style="place-content: center" class="tableView">
              <el-empty description="请选择教学楼" />
            </el-row>
          </el-row>
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-else-if="checkboxGroup.length == 0"
          >
            <el-row style="place-content: center" class="tableView">
              <el-empty description="请选择节次" />
            </el-row>
          </el-row>
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-else-if="ans.length == 0"
          >
            <el-row style="place-content: center" class="tableView">
              <el-empty description="没有空教室了😢" />
            </el-row>
          </el-row>
          <el-row style="place-content: center; margin-bottom: 20px" v-else>
            <el-row style="place-content: center" class="tableView">
              <el-table :data="ans" stripe>
                <el-table-column prop="room" label="教室" />
                <el-table-column label="类型">
                  <template #default="{ row }">
                    {{ typeMap[row.room] ?? "无数据" }}
                  </template>
                </el-table-column>
                <el-table-column prop="num" label="座位数" />
              </el-table>
            </el-row>
          </el-row>
          <el-row
            style="place-content: center; margin-bottom: 20px"
            v-if="hasAdvice"
          >
            <el-row style="place-content: center" class="tableView">
              <div
                style="
                  margin: 20px;
                  margin-bottom: 0px;
                  color: var(--el-text-color-secondary);
                  font-size: var(--el-font-size-base);
                "
              >
                教室较少，智能推荐以下方案：
              </div>
              <div
                style="
                  margin: 20px;
                  margin-bottom: 0px;
                  color: var(--el-text-color-secondary);
                  font-size: var(--el-font-size-base);
                "
                v-for="single_advice in advice"
                :key="single_advice[0][0]"
              >
                从第{{ single_advice[0][0] }}节到第{{
                  single_advice[0][single_advice[0].length - 1]
                }}节，可选教室：
                <el-tag
                  v-for="room in single_advice[1]"
                  :key="room"
                  style="margin: 5px"
                  >{{ room["room"] }}</el-tag
                >
              </div>
              <div style="margin-bottom: 20px"></div>
            </el-row>
          </el-row>
        </div>
        <el-row
          style="place-content: center; margin-bottom: 20px"
          v-if="apiError"
        >
          <el-row style="place-content: center">
            <el-empty
              description="数据获取失败，请刷新重试，如果仍失败请在说明中提交反馈"
            />
          </el-row>
        </el-row>
        <el-row style="place-content: center; margin-bottom: 20px">
          <el-row style="place-content: center">
            <div
              style="
                color: var(--el-text-color-secondary);
                font-size: var(--el-font-size-base);
              "
            >
              © 2022-2023 Jray
              <a href="https://github.com/Jraaay/empty-classroom-public"
                >Github</a
              >
            </div>
          </el-row>
        </el-row>
      </el-col>
    </el-container>
    <el-dialog
      v-model="dialogVisible"
      style="width: 90%; max-width: 400px"
      title="设置"
      @close="openLogClickTime = 0"
    >
      <div style="margin-top: 2px">
        <el-switch v-model="showTime" active-text="显示课程时间" />
      </div>
      <el-divider @click="openLog">
        <el-icon><StarFilled /></el-icon>
      </el-divider>
      <div style="line-height: 2em">当前版本：{{ version }}</div>
      <div style="line-height: 2em">
        数据来源：微教务的空教室查询、教务系统的教室课表
      </div>
      <div style="line-height: 2em">
        只能获取当天数据，次日数据请次日零点后查询
      </div>
      <div style="line-height: 2em">全部可用网址：</div>
      <div style="line-height: 2em">
        <a href="https://sleep.jray.xyz"> https://ec.jray.xyz </a>
      </div>
      <div style="line-height: 2em">
        <a href="https://sleep.jray.xyz"> https://sleep.jray.xyz </a>
      </div>
      <div style="line-height: 2em">
        <a href="https://classroom.jray.xyz"> https://classroom.jray.xyz </a>
      </div>
      <div style="line-height: 2em">
        当前数据刷新时间：{{
          empty_rooms.time?.split(":").splice(0, 2).join(":")
        }}
      </div>
      <div style="line-height: 2em">
        项目已开源：
        <a href="https://github.com/Jraaay/empty-classroom-public"> Github </a>
      </div>
    </el-dialog>
    <el-dialog v-model="logVisible" title="日志" class="logDialog">
      <el-timeline style="padding: 0px">
        <el-timeline-item
          v-for="logItem of logContent"
          :key="logItem"
          :type="logItem.type"
          :timestamp="logItem.time.toString()"
        >
          {{ logItem.message }}
        </el-timeline-item>
      </el-timeline>
      <!-- <p v-for="logItem of logContent" :key="logItem">{logItem}</p> -->
    </el-dialog>
  </div>
</template>

<script>
import { usePreferredDark, useDark } from "@vueuse/core";
import * as Sentry from "@sentry/vue";
import { InfoFilled, Opportunity } from "@element-plus/icons-vue";
import { shallowRef } from "vue";
import { config } from "../config";
export default {
  setup() {
    console.log(
      "start setup at " +
        new Date().toLocaleString() +
        "." +
        new Date().getMilliseconds()
    );
    useDark(usePreferredDark());
  },
  data() {
    return {
      version: config.version,
      hasNewVer: false,
      newVer: "",
      classes: [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
      ],
      class_time: [
        "08:45",
        "09:35",
        "10:35",
        "11:25",
        "12:15",
        "13:45",
        "14:35",
        "15:30",
        "16:25",
        "17:20",
        "18:10",
        "19:15",
        "20:05",
        "20:55",
      ],
      class_start_time: [
        "08:00",
        "08:50",
        "09:50",
        "10:40",
        "11:30",
        "13:00",
        "13:50",
        "14:45",
        "15:40",
        "16:35",
        "17:25",
        "18:30",
        "19:20",
        "20:10",
      ],
      checkboxGroup: [],
      empty_rooms: {},
      ans: [],
      campus_id: "西土城",
      checkAll: false,
      building: [],
      building_all: [],
      building_xtc: [],
      building_sh: [],
      hasAdvice: false,
      advice: [],
      loading: true,
      apiError: false,
      notification: null,
      Info: shallowRef(InfoFilled),
      Opportunity: shallowRef(Opportunity),
      showTime: true,
      dialogVisible: false,
      openLogClickTime: 0,
      logVisible: false,
      logContent: [],
      typeMap: {},
      trustBuilding: ["教1", "教2", "教3", "教4", "图书馆", "S1", "N", "S"],
    };
  },
  created() {
    console.log(
      "created at " +
        new Date().toLocaleString() +
        "." +
        new Date().getMilliseconds()
    );
    this.getEmptyRooms();
  },
  mounted() {
    console.log(
      "mounted at " +
        new Date().toLocaleString() +
        "." +
        new Date().getMilliseconds()
    );
  },
  beforeMount() {
    this.showTime = (localStorage.getItem("showTime") ?? "true") == "true";
    console.log(this.showTime);
  },
  methods: {
    getEmptyRooms() {
      console.log(
        "start get api at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      fetch("/api")
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            console.log(res);
            throw new Error(res.statusText + " " + res.status);
          }
        })
        .then((data) => {
          console.log("api response time at " + data?.time);
          this.empty_rooms = data;
          this.typeMap = data["class_list"]["type_map"];
          this.loading = false;
          this.apiError = false;
          if (
            this.empty_rooms["class_list"] == undefined ||
            this.empty_rooms["class_list"] == null ||
            this.empty_rooms["class_list"].length == 0
          ) {
            ElNotification({
              title: "数据获取错误",
              message:
                "服务端获取空教室数据失败，可能是教务系统出现问题或者接口更新，请反馈并等待更新。",
              type: "error",
              duration: 5000,
            });
          } else {
            this.building_xtc = [];
            for (let i of this.empty_rooms["class_list"]["1"]) {
              for (let j of i) {
                if (!this.building_xtc.includes(j[0].split("-")[0])) {
                  this.building_xtc.push(j[0].split("-")[0]);
                }
              }
            }
            this.building_xtc.sort((a, b) => {
              return a.length - b.length;
            });
            this.building_sh = [];
            for (let i of this.empty_rooms["class_list"]["2"]) {
              for (let j of i) {
                if (!this.building_sh.includes(j[0].split("-")[0])) {
                  this.building_sh.push(j[0].split("-")[0]);
                }
              }
            }
            this.building_sh.sort((a, b) => {
              return a.length - b.length;
            });
            this.building_all =
              this.campus_id == "西土城" ? this.building_xtc : this.building_sh;
          }
          if (
            data?.notification &&
            (data?.notification.showNotification ?? false)
          ) {
            console.log(
              "auto show notification at " +
                new Date().toLocaleString() +
                "." +
                new Date().getMilliseconds()
            );
            ElNotification({
              title: data.notification.title ?? "提示",
              dangerouslyUseHTMLString: true,
              message: data.notification.content.replace(/\n/g, "<br>"),
              type: data.notification.type ?? "info",
              duration: data.notification.duration ?? 4500,
            });
          }
          this.notification = data?.notification;
          if (data?.version && data.version > this.version) {
            this.hasNewVer = true;
            this.newVer = data.version;
          }
        })
        .catch((err) => {
          console.log("api err: " + err);
          ElNotification({
            title: "获取数据失败，请刷新重试或者在说明中提交反馈",
            message: err.message,
            type: "error",
          });
          this.loading = false;
          this.apiError = true;
        })
        .finally(() => {
          console.log(
            "api finish at " +
              new Date().toLocaleString() +
              "." +
              new Date().getMilliseconds()
          );
        });
    },
    update_ans() {
      if (this.loading) {
        return false;
      }
      console.log(
        "start update ans at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      this.ans = this.getEmpty.call(this, this.checkboxGroup);
      this.ans.sort((a, b) => {
        return a.room.localeCompare(b.room);
      });
      console.log(
        "finish getEmpty at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      if (this.building.length == 0 || this.checkboxGroup.length == 0) {
        this.hasAdvice = false;
        return;
      }
      let include_advice_building = 0;
      if (this.building.includes("教3")) {
        include_advice_building += 1;
      }
      if (this.building.includes("S")) {
        include_advice_building += 1;
      }
      if (this.building.includes("N")) {
        include_advice_building += 1;
      }
      if (this.building.includes("S1")) {
        include_advice_building += 1;
      }
      if (this.ans.length < 10 * include_advice_building) {
        this.getAdvice();
      } else {
        this.hasAdvice = false;
      }
      console.log(
        "finish get advice at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
    },
    handleCheckAllChange() {
      console.log(
        "check all change at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      if (this.loading) {
        return false;
      }
      if (!this.checkedAll()) {
        this.checkboxGroup = [];
        for (let i = 0; i < 14; i++) {
          if (
            !(
              !(
                new Date().getHours() > 20 ||
                (new Date().getHours() == 20 && new Date().getMinutes() >= 55)
              ) &&
              (new Date().getHours() >
                parseInt(this.class_time[i].split(":")[0]) ||
                (new Date().getHours() ==
                  parseInt(this.class_time[i].split(":")[0]) &&
                  new Date().getMinutes() >=
                    parseInt(this.class_time[i].split(":")[1])))
            )
          ) {
            this.checkboxGroup.push(this.classes[i]);
          }
        }
      } else {
        this.checkboxGroup = [];
      }
    },
    checkedAll() {
      let ans = true;
      for (let i = 0; i < 14; i++) {
        if (
          !(
            (!(
              new Date().getHours() > 20 ||
              (new Date().getHours() == 20 && new Date().getMinutes() >= 55)
            ) &&
              new Date().getHours() >
                parseInt(this.class_time[i].split(":")[0])) ||
            (new Date().getHours() ==
              parseInt(this.class_time[i].split(":")[0]) &&
              new Date().getMinutes() >=
                parseInt(this.class_time[i].split(":")[1]))
          )
        ) {
          if (this.checkboxGroup.findIndex((x) => x == this.classes[i]) == -1) {
            ans = false;
            break;
          }
        }
      }
      return ans;
    },
    getAdvice() {
      if (this.loading) {
        return false;
      }
      this.hasAdvice = true;
      const classes = this.checkboxGroup.sort();
      this.advice = [];
      let cur = 1;
      let last_end = 0;
      let cur_classroom = this.getEmpty.call(
        this,
        classes.slice(last_end, last_end + cur)
      );
      let fir_classroom = cur_classroom;
      for (let i = 1; i < classes.length; i++) {
        const tmp_classroom = this.getEmpty.call(
          this,
          classes.slice(last_end, i + 1)
        );
        const tmp2_classroom = this.getEmpty.call(
          this,
          classes.slice(i, i + 2)
        );
        if (
          (cur >= 2 &&
            (tmp_classroom.length < (fir_classroom.length / 3) * 2 ||
              cur_classroom.length < (tmp2_classroom.length / 3) * 1)) ||
          (parseInt(classes[i]) - parseInt(classes[i - 1]) > 1 &&
            tmp_classroom.length < (fir_classroom.length / 3) * 2)
        ) {
          this.advice.push([classes.slice(last_end, i), cur_classroom]);
          last_end = i;
          cur = 1;
          cur_classroom = this.getEmpty.call(
            this,
            classes.slice(last_end, last_end + cur)
          );
          fir_classroom = cur_classroom;
        } else {
          cur += 1;
          cur_classroom = tmp_classroom;
        }
      }
      this.advice.push([classes.slice(last_end), cur_classroom]);
      for (let i = 0; i < this.advice.length - 1; i++) {
        if (this.advice[i][1].every((x) => this.advice[i + 1][1].includes(x))) {
          this.advice[i][0] = this.advice[i][0].concat(this.advice[i + 1][0]);
          this.advice.splice(i + 1, 1);
        }
      }
    },
    getEmpty(selected_class) {
      const tmp_campus = this.campus_id == "西土城" ? "1" : "2";
      var tmp_ans = new Set(
        this.empty_rooms["class_list"][tmp_campus][
          parseInt(selected_class[0]) - 1
        ]
      );
      for (let class_id of selected_class) {
        if (class_id === false) {
          continue;
        }
        const tmp_set = new Set(
          [
            ...this.empty_rooms["class_list"][tmp_campus][
              parseInt(class_id) - 1
            ],
          ].map((x) => x[0])
        );
        tmp_ans = new Set([...tmp_ans].filter((x) => tmp_set.has(x[0])));
      }
      tmp_ans = new Set(
        [...tmp_ans].filter((x) => this.building.includes(x[0].split("-")[0]))
      );
      return [...tmp_ans].map((x) => {
        return {
          room: x[0],
          num: x[1],
        };
      });
    },
    async report() {
      let input;
      try {
        input = await ElMessageBox.prompt(
          "请在下方输入您的反馈。程序日志将被同时提交，建议附上邮箱以便回复。",
          "反馈提交",
          {
            inputType: "textarea",
            inputPlaceholder: "此处填写反馈信息",
          }
        );
      } catch (e) {
        return;
      }
      if (!input.value) return;
      const comments = input.value;
      const evid = Sentry.captureMessage("用户反馈：\n" + comments);
      const dsn = config.sentryDsn;
      const u = new URL(dsn);
      u.username = "";
      u.password = "";
      u.pathname =
        u.pathname.split("/").slice(0, -1).join("/") + "/api/embed/error-page/";
      u.searchParams.set("eventId", evid);
      u.searchParams.set("dsn", dsn);
      const reportData = {
        name: "anonymous-report",
        email: `anonymous-report@jray.xyz`,
        comments,
      };
      try {
        const res = await fetch(u.toString(), {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams(reportData).toString(),
        });
        if (res.ok) {
          ElNotification({
            title: "日志已上传",
            message: "反馈提交成功",
            type: "success",
            customClass: "feedback-notification",
            duration: 0,
          });
        } else {
          throw new Error("Got a non-200 response");
        }
      } catch (e) {
        ElNotification({
          title: "反馈提交失败",
          message: e.message,
          type: "error",
        });
      }
    },
    showNotification() {
      if (this.loading) {
        return;
      }

      console.log(
        "manually show notification at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      ElNotification({
        title: this.notification.title ?? "提示",
        dangerouslyUseHTMLString: true,
        message: this.notification.content.replace(/\n/g, "<br>"),
        type: this.notification.type ?? "info",
        duration: this.notification.duration ?? 4500,
      });
    },
    showUpdate() {
      ElMessageBox.confirm(
        "接下来页面将会刷新，为你更新到新版本，如果更新失败，请手动多次刷新页面直至更新成功",
        "版本更新（Beta）",
        {
          confirmButtonText: "好",
          cancelButtonText: "下次吧",
          type: "success",
        }
      )
        .then(() => {
          location.reload(true);
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消更新",
          });
        });
    },
    openLog() {
      this.openLogClickTime++;
      if (
        this.openLogClickTime == 5 ||
        localStorage.getItem("admin") == "true"
      ) {
        ElMessageBox.prompt("请输入密码", "日志", {
          confirmButtonText: "查看",
          cancelButtonText: "取消",
        })
          .then(({ value }) => {
            if (value == "" || value == null) {
              value = localStorage.getItem("logpwd") ?? "";
            } else {
              localStorage.setItem("logpwd", value);
            }
            fetch("/api/get-log?pwd=" + value, {
              method: "POST",
            })
              .then((res) => {
                if (res.ok) {
                  return res.text();
                } else {
                  ElMessage.error("验证失败");
                }
              })
              .then((data) => {
                localStorage.setItem("admin", "true");
                const tmp = data.split("\n");
                this.logContent = [];
                for (let log of tmp) {
                  if (
                    log != "" &&
                    /\[\d+-\d+-\d+\s\d+:\d+:\d+,\d+\]\s\[[^\]]*\]\s\[[^\]]*\].*/.test(
                      log
                    )
                  ) {
                    const logList = log.split(" ");
                    const info = {};
                    info.time =
                      logList[0].replace("[", "") +
                      " " +
                      logList[1].replace("]", "");
                    info.type =
                      logList[3] == "[INFO]"
                        ? "info"
                        : logList[3] == "[ERROR]"
                        ? "danger"
                        : "warning";
                    logList.splice(0, 3);
                    info.message = logList.join(" ");
                    this.logContent.push(info);
                  }
                }
                this.logContent = this.logContent.reverse();
                this.logVisible = true;
              });
          })
          .catch(() => {
            ElMessage({
              type: "info",
              message: "false",
            });
          });
      }
    },
  },
  watch: {
    checkboxGroup(val) {
      console.log(
        "checkboxGroup change: " +
          val +
          " at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      if (this.loading) {
        return false;
      }
      this.update_ans();
    },
    campus_id(val) {
      console.log(
        "campus_id change: " +
          val +
          " at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      this.hasAdvice = false;
      this.building_all =
        this.campus_id == "西土城" ? this.building_xtc : this.building_sh;
      this.building = [];
      if (this.loading) {
        return false;
      }
      this.update_ans();
    },
    building(val) {
      console.log(
        "building change: " +
          val +
          " at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      if (this.loading) {
        return false;
      }
      this.hasAdvice = false;
      this.update_ans();
    },
    showTime(val) {
      console.log(
        "showTime change: " +
          val +
          " at " +
          new Date().toLocaleString() +
          "." +
          new Date().getMilliseconds()
      );
      localStorage.setItem("showTime", val);
    },
  },
};
</script>

<style scoped>
.tableView {
  box-shadow: 0px 12px 32px 4px rgba(0, 0, 0, 0.04),
    0px 8px 20px rgba(0, 0, 0, 0.08);
  width: 90%;
  max-width: 400px;
  border-radius: 6px;
}

.checkgroupView {
  box-shadow: 0px 12px 32px 4px rgba(0, 0, 0, 0.04),
    0px 8px 20px rgba(0, 0, 0, 0.08);
}

.checkAll {
  width: 50px;
  border: 0px;
  border-radius: 0px;
  margin-left: 1px;
  height: 30px;
}

.title {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif !important;
}

div {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif !important;
}
</style>

<style>
.cell {
  text-align: center;
}

.el-checkbox-button__inner {
  border-radius: 4px !important;
  border: 0px !important;
  min-width: 50px;
  margin: 1px;
  box-shadow: none !important;
  border-radius: 0px !important;
}

.el-radio-button__inner {
  border-radius: 0px !important;
}

.el-collapse {
  --el-collapse-border-color: transparent !important;
}

.el-checkbox-button__inner {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 2px;
  padding-right: 2px;
  text-align: -webkit-center;
}

.el-dialog {
  width: 90%;
  max-width: 400px;
  border-radius: 4px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif !important;
}

.el-dialog__header {
  padding-top: 15px;
}

.el-dialog__headerbtn {
  top: 0px;
}

.el-dialog__body {
  padding-top: 0px;
  padding-bottom: 16px;
}

.el-divider--horizontal {
  margin: 10px 0px;
}

.el-message-box {
  margin: var(--el-dialog-margin-top, 15vh) auto 50px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif !important;
}

.el-overlay.is-message-box .el-overlay-message-box {
  top: 0px;
  bottom: 0px;
  position: unset;
}

.pick-building
  > .el-checkbox-group
  > .el-checkbox-button
  > .el-checkbox-button__inner {
  min-width: 100px;
  width: fit-content;
  padding-left: 10px;
  padding-right: 10px;
}
</style>