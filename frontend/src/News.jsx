import Post from "./Post.jsx";

function News() {
  const post = {
    title: "test",
    body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris." +
      " Vivamus hendrerit arcu sed erat molestie vehicula. " +
      "Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. " +
      "Ut in nulla enim. Phasellus molestie magna non est bibendum non " +
      "venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus.",
    image: "https://st.getinfootball.com/news/1073716/65688d9f87fe9_910x610.jpg"
  };
  return (
    <ul className="news">
      <li><Post post={post}/></li>
      <li><Post post={post}/></li>
      <li><Post post={post}/></li>
    </ul>
  );
}

export default News;
