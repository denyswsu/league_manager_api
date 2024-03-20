

function Post({ post }) {
  return (
    <div className="post">
      <img className="post-image" alt="Post Image" src={post.image}></img>
      <h2 className="post-title">{post.title}</h2>
      <p className="post-text">{post.body}</p>
    </div>
  );
}

export default Post;
