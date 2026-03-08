export const meta = {
  id: "hn.favorites",
  version: "1.0.0",
  title: "HN Favorites",
  allowed_domains: ["news.ycombinator.com"]
};

export async function run(ctx) {
  await ctx.navigate("https://news.ycombinator.com/favorites?id=<user>");
  await ctx.paginate({ next: "a.morelink", max_pages: 25, max_runtime_seconds: 180 });
  await ctx.collect_links({ selectors: ["a.storylink", "span.titleline > a"] });
}
