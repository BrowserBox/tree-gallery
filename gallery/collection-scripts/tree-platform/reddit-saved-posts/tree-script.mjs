export const meta = {
  id: "reddit.saved_posts",
  version: "1.0.0",
  title: "Reddit Saved Posts",
  requires_auth: true,
  allowed_domains: ["reddit.com", "www.reddit.com"]
};

export async function run(ctx) {
  await ctx.navigate("https://www.reddit.com/user/me/saved/");
  await ctx.paginate({ next: "a[rel='nofollow next']", max_pages: 20, max_runtime_seconds: 240 });
  await ctx.collect_links({ selectors: ["a[data-click-id='body']", "a[data-click-id='comments']"] });
}
