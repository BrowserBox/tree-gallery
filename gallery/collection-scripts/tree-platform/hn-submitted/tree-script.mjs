export const meta = {
  id: "hn.submitted",
  version: "1.0.0",
  title: "HN Submitted",
  allowed_domains: ["news.ycombinator.com"]
};

export async function run(ctx) {
  await ctx.navigate("https://news.ycombinator.com/submitted?id=<user>");
  await ctx.paginate({ next: "a.morelink", max_pages: 25, max_runtime_seconds: 180 });
  await ctx.collect_links({ selectors: ["a.storylink", "span.titleline > a"] });
}
