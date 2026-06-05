from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from database import get_db
from schemas import PostResponse, PostCreate, PostUpdate

from auth import CurrentUser


router = APIRouter()


# GET /api/posts - Get all posts
@router.get("", response_model=list[PostResponse])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc())
    )
    posts = result.scalars().all()
    return posts


# GET /api/posts/{post_id} - Get post details
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalars().first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


# POST /api/posts - Create a new post
@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    new_post = models.Post(
        title=post.title, content=post.content, user_id=current_user.id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])
    return new_post


# PUT /api/posts/{post_id} - Update post details (full update)
@router.put("/{post_id}", response_model=PostResponse)
async def update_post_full(
    post_id: int,
    post_data: PostCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    existing_post = result.scalars().first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if existing_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post",
        )

    existing_post.title = post_data.title
    existing_post.content = post_data.content
    existing_post.user_id = current_user.id

    await db.commit()
    await db.refresh(existing_post, attribute_names=["author"])
    return existing_post


# PATCH /api/posts/{post_id} - Update post details (partial update)
@router.patch("/{post_id}", response_model=PostResponse)
async def update_post_partial(
    post_id: int,
    post_data: PostUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    existing_post = result.scalars().first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if existing_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post",
        )

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_post, field, value)

    await db.commit()
    await db.refresh(existing_post, attribute_names=["author"])
    return existing_post


# DELETE /api/posts/{post_id} - Delete a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    existing_post = result.scalars().first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if existing_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post",
        )

    await db.delete(existing_post)
    await db.commit()
