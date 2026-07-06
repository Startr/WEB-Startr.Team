module.exports = function (eleventyConfig) {
  // Pass through static assets
  eleventyConfig.addPassthroughCopy("**/*.{png,jpg,jpeg,gif,svg,webp,ico,avif}");
  // Scoped to assets/ so build-time modules in _data/ never ship into _site.
  eleventyConfig.addPassthroughCopy("assets/**/*.css");
  eleventyConfig.addPassthroughCopy("assets/**/*.js");
  eleventyConfig.addPassthroughCopy("assets/**/*.{woff,woff2}"); // vendored System 7 fonts

  return {
    dir: {
      input: ".",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
};
