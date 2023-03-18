import { createApp } from 'vue';
import App from './App.vue';
import { init } from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";
import 'element-plus/theme-chalk/dark/css-vars.css';
import { ChatLineSquare, Setting, StarFilled } from '@element-plus/icons-vue';
import { config } from "../config";

const app = createApp(App);
app.component("ChatLineSquare", ChatLineSquare);
app.component("Setting", Setting);
app.component("StarFilled", StarFilled);

app.mount('#app');

const ignoredFunctions = new Set([
  "is_mark_able_element",
  "findParentClickTag",
  "close_cache_key",
  "check_swipe_element",
  "eval",
]);

// 初始化 Sentry
init({
  app,
  dsn: config.sentryDsn,
  integrations: [
    new BrowserTracing({
      tracingOrigins: ["localhost", "https://ec.jray.xyz", /^\//],
    }),
  ],
  release: config.version,
  tracesSampleRate: 1.0,
  ignoreErrors: [
    "this.hostIndex.push is not a function",
    "undefined is not an object (evaluating 't.uv')",
    "SyntaxError: The string did not match the expected pattern.",
    "instantSearchSDKJSBridgeClearHighlight",
    "window.bannerNight",
    "window.ucbrowser",
    "webkitExitFullScreen",
    "close_cache_key",
    "UCShellJava",
    "file:///",
    "hw-upgrade-client",
    "is_mark_able_element",
    "QK_middlewareReadModePageDetect",
    "window.webkit.messageHandlers",
    "Timeout to initialize runtime",
    "this.excludedTags.length",
  ],
  denyUrls: [/^chrome-extension:\/\//i, /^moz-extension:\/\//i, /^safari-extension:\/\//i, /^file:\/\//i],
  autoSessionTracking: true,
  beforeSend: (event, hint) => {
    if (event?.exception?.values?.[0]?.stacktrace?.frames?.some((x) => ignoredFunctions.has(x?.function || ""))) {
      return null;
    }
    if (
      hint?.originalException &&
      typeof hint.originalException !== "string" &&
      /Loading chunk \d+ failed after \d+ retries/.test(hint.originalException.message)
    ) {
      event.fingerprint = ["ChunkLoadError"];
    }
    return event;
  },
});