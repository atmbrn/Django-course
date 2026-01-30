function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");


$(document).on("click", ".add-comment", function (e) {
    e.preventDefault();
    const postId = $(this).data("post-id");
    const input = $(`input.comment-input[data-post-id="${postId}"]`);
    const text = input.val().trim();

    if (!text) {
        alert("Please enter a comment");
        return;
    }

    $.ajax({
        url: "/shop/posts/comment/add/",
        method: "POST",
        data: {
            post_id: postId,
            text: text,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            const emptyMessage = $(`#empty-comments-${postId}`);
            if (emptyMessage.length) {
                emptyMessage.remove();
            }

            const newCommentHtml = `
                <li class="list-group-item" id="comment-${response.id}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            ${response.text}
                            <br>
                            <small class="text-muted">just now</small>
                        </div>
                        <button class="btn btn-sm btn-outline-danger delete-comment" data-id="${response.id}">Delete</button>
                    </div>
                </li>
            `;
            $(`#comments-list-${postId}`).append(newCommentHtml);

            $(`#comments-count-${postId}`).text(response.comments_count);

            input.val("");
        },
        error: function (xhr) {
            alert("Error adding comment");
            console.error(xhr.responseText);
        },
    });
});

$(document).on("click", ".delete-comment", function (e) {
    e.preventDefault();
    const commentId = $(this).data("id");
    const commentElement = $(`#comment-${commentId}`);

    const commentsList = commentElement.closest("ul");
    const postId = commentsList.attr("id").replace("comments-list-", "");

    if (confirm("Are you sure you want to delete this comment?")) {
        $.ajax({
            url: `/shop/posts/comment/${commentId}/delete/`,
            method: "POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (response) {
                commentElement.remove();

                const newCount = response.comments_count;
                $(`#comments-count-${postId}`).text(newCount);

                if (newCount === 0) {
                    const emptyMessage = `<li class="list-group-item" id="empty-comments-${postId}">No comments yet.</li>`;
                    commentsList.html(emptyMessage);
                }
            },
            error: function (xhr) {
                alert("Error deleting comment");
                console.error(xhr.responseText);
            },
        });
    }
});

$(document).on("click", ".like-button", function (e) {
    e.preventDefault();
    const postId = $(this).data("id");

    $.ajax({
        url: `/shop/posts/${postId}/like/`,
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $(`#likes-count-${postId}`).text(response.likes);
            $(`#dislikes-count-${postId}`).text(response.dislikes);
        },
        error: function (xhr) {
            alert("Error liking post");
            console.error(xhr.responseText);
        },
    });
});

$(document).on("click", ".dislike-button", function (e) {
    e.preventDefault();
    const postId = $(this).data("id");

    $.ajax({
        url: `/shop/posts/${postId}/dislike/`,
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $(`#likes-count-${postId}`).text(response.likes);
            $(`#dislikes-count-${postId}`).text(response.dislikes);
        },
        error: function (xhr) {
            alert("Error disliking post");
            console.error(xhr.responseText);
        },
    });
});

$(document).on("keypress", ".comment-input", function (e) {
    if (e.which === 13) {
        e.preventDefault();
        const postId = $(this).data("post-id");
        $(`.add-comment[data-post-id="${postId}"]`).click();
    }
});
