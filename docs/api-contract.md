# Canonical API contract

The API is rooted at `/api`. JSON property names are camelCase.

## Conventions

- Authentication uses `Authorization: Bearer <token>`.
- Content types are `article`, `video`, `audio`, and `image`.
- Content statuses are `draft`, `published`, and `archived`.
- Public content endpoints return only approved, published content.
- IDs are integers.
- Validation errors use `{ "error": "..." }`.

## Authentication

| Method | Endpoint | Auth | Body |
| --- | --- | --- | --- |
| POST | `/auth/register` | No | `{ username, email, password }` |
| POST | `/auth/login` | No | `{ identifier, password }` |
| GET | `/auth/me` | Yes | — |
| POST | `/auth/logout` | No | — |
| POST | `/auth/forgot-password` | No | `{ email }` |
| POST | `/auth/reset-password` | No | `{ token, password }` |

Register and login return `{ token, user }`.

## Content

| Method | Endpoint | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/content` | No | Published feed; supports `category` and `search` |
| GET | `/content/:id` | Optional | Read published content; owners/admins can read drafts |
| POST | `/content` | Yes | Submit a draft |
| PATCH | `/content/:id` | Yes | Update content owned by the user or moderated by staff |
| DELETE | `/content/:id` | Yes | Delete own content or admin content |
| GET | `/content/:id/reactions` | Optional | Reaction summary |
| POST | `/content/:id/reactions` | Yes | Toggle `like` or `dislike` |
| GET | `/content/:id/comments` | No | Threaded comments |
| POST | `/content/:id/comments` | Yes | `{ body, parentId? }` |
| PATCH | `/comments/:id` | Yes | `{ body }` |
| DELETE | `/comments/:id` | Yes | Delete a comment |
| POST | `/content/:id/report` | Yes | `{ reason }` |
| POST | `/content/:id/share` | Yes | `{ sharedWithUserId }`; records a share |
| POST | `/comments/:id/reactions` | Yes | Toggle `{ type: "like" | "dislike" }` |
| DELETE | `/comments/:id/reactions` | Yes | Remove the current user's reaction |

Content objects have this shape:

```json
{
  "id": 1,
  "title": "A practical guide",
  "body": "...",
  "type": "article",
  "mediaUrl": null,
  "status": "published",
  "isApproved": true,
  "createdAt": "2026-09-04T10:00:00+00:00",
  "updatedAt": "2026-09-04T10:00:00+00:00",
  "author": { "id": 2, "username": "dev", "role": "user", "isActive": true },
  "categories": [{ "id": 3, "name": "Backend" }],
  "likesCount": 3,
  "dislikesCount": 0,
  "commentsCount": 2,
  "viewsCount": 0
}
```

## Categories and preferences

| Method | Endpoint | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/categories` | No | List categories |
| POST | `/categories` | Admin/tech writer | Create category |
| PATCH | `/categories/:id` | Admin/tech writer | Update category |
| DELETE | `/categories/:id` | Admin | Delete an unused category |
| GET | `/subscriptions` | Yes | Current user's subscriptions |
| POST | `/subscriptions` | Yes | `{ categoryId }` |
| DELETE | `/subscriptions/:categoryId` | Yes | Unsubscribe |
| GET | `/wishlist` | Yes | Current user's saved content |
| POST | `/wishlist` | Yes | `{ contentId }` |
| DELETE | `/wishlist/:contentId` | Yes | Remove saved content |

## Profile and notifications

| Method | Endpoint | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/users/me` | Yes | Current user's account fields |
| PUT | `/users/me` | Yes | Update username, email, or password |
| GET | `/profiles/me` | Yes | Current user's profile |
| PUT | `/profiles/me` | Yes | Update profile fields |
| GET | `/notifications` | Yes | Current user's notifications |
| PATCH | `/notifications/:id/read` | Yes | Mark one notification read |
| PATCH | `/notifications/read-all` | Yes | Mark all notifications read |

## Administration

All admin endpoints require the `admin` role.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/admin/content?status=draft` | Content moderation queue |
| PATCH | `/admin/content/:id/status` | Set `draft`, `published`, or `archived`; `{ status, reason? }` |
| DELETE | `/admin/content/:id` | Delete content |
| GET | `/admin/users` | List users |
| POST | `/admin/users` | Create a user |
| PATCH | `/admin/users/:id/status` | Toggle active status |
| GET | `/admin/reports` | List reports |
| PATCH | `/admin/reports/:id` | Resolve a report |
