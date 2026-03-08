export const meta = {
  id: "reading_queue.import",
  version: "1.0.0",
  title: "Reading Queue Import",
  allowed_domains: []
};

export async function run(ctx) {
  const urls = Array.isArray(ctx.input_urls) ? ctx.input_urls : [];
  for (const url of urls) {
    await ctx.navigate(url);
    await ctx.wait_for({ ms: 1500 });
  }
}
