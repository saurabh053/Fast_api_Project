from fastapi import APIRouter, HTTPException
from social_media_app.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

post_table = {}
comments_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()  # previously .dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()  # previously .dict()
    last_record_id = len(comments_table)
    new_comment = {**data, "id": last_record_id}
    comments_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comments_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }


# # decorator is a way to extend the functionality of function
# # app decorator tells that whenever app receives a request and that request is made at this endpoint then this function
# # should run and whatever this function returns should be sent back to the client
# # A client in this case may be a website or a mobile app that wants to request some data from our API so they are going to send us a request
# @router.get("/")
# # Async in-front of a function just means that this function can run more or less at the same time as other functions. If any of the functions that we are
# # trying to run at the same time do heavy computation then they can't run at the same time but if they are all just waiting for the client to send us some
# # data or they are waiting for the client tio send us some data or they are waiting for the database to respond to our requests or things that then those
# # functions can run in parallel more or less. So that is where we get a speed benefit when we use FastAPI and async functions
# async def root():
#     return {"message": "Hello World"}
#
#
