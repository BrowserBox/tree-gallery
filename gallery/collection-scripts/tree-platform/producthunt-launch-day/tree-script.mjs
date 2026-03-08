export const meta = {
  id: "producthunt.launch_day",
  version: "1.0.0",
  title: "Product Hunt Launch Day",
  allowed_domains: ["producthunt.com", "www.producthunt.com"]
};

export async function run(ctx) {
  await ctx.navigate("https://www.producthunt.com/posts/<slug>");
  await ctx.wait_for({ selector: "main", timeout_ms: 15000 });
  await ctx.collect_links({ selectors: ["main a", "a[href*='/posts/']"] });
}
