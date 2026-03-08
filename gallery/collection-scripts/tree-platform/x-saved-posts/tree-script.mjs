export const meta = {
  id: "x.saved_posts",
  version: "1.0.0",
  title: "X Saved Posts",
  requires_auth: true,
  allowed_domains: ["x.com", "twitter.com"]
};

export async function run(ctx) {
  await ctx.navigate("https://x.com/i/bookmarks");
  await ctx.scroll_collect({ max_scrolls: 80, idle_ms: 1200, max_runtime_seconds: 300 });
  await ctx.collect_links({ selectors: ["article a[href*='/status/']"] });
}
