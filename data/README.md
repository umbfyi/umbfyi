# Data Repository

UMB.FYI relies on some external data sources to function. In the name of keeping things simple, these are simple JSON files stored here in order to allow people to easily contribute to them.

## `profiles.json`

The `profiles.json` files is what defines the user profile details for content creators featured in UMB.FYI. A profile provides content creators with a dedicated URL that displays an ever updating timeline of all their featured content.

To add your profile submit a PR with an update to `profiles.json` file adding a profile entry to the root array. Profiles should be added in alphabetical order by alias so please insert your profile in the appropriate location.

The properties of the profile object are as follows:

| Property | Description |
| -- | -- |
| `alias` | A URL safe, all lowercase alias for your profile. This is used to constuct your profile URL in the format `https://umb.fyi/@{alias}`. Please make sure your alias is unique. |
| `name` | The display name for you profile. |
| `description` | A short description / bio for you profile. |
| `url` | A primary URL to link to from your profile. |
| `avatar` | The URL to an image to display as your avatar. Avatars are displayed in a circular form with a white border. |
| `sources` | A list of media sources owned by this account. When UMB.FYI parses media from feeds, it will match the media source with a source from a profile to link media ownership. See information about [Sources](#sources) below. |

### Sources
An important concept to understand when linking a profile to content is the source of a given media item. Because it is important, I've listed below how to obtain the source URL for common feed types and the fallback we use as a last resort.

#### RSS feed
For RSS feeds the source is the URL found in the `<link>` tag of the channel.

#### YouTube feed
You can follow the same rule of thumb for RSS feeds, but it will effectively be in the format `https://www.youtube.com/channel/{channelId}` where `channelId` is your non-friendly channel identifier (ie `UCcltXlJQ-U553MoOsP9p4wg`)

#### Mastodon
For mastodon, the source will be your mastodon account URL ie `https://umbracocommunity.social/@matt`

#### DEV.to blog
Fro DEV.to blogs, the source will be your profile URL for you account ie `https://dev.to/mattbrailsford`

#### Hashnode blog
Fro Hashnode blogs, the source will be your profile URL for you account ie `https://mattbrailsford.hashnode.dev`

#### Medium blog
Fro Medium blogs, the source will be your profile URL for you account ie `https://mattbrailsford.medium.com` or `https://medium.com/@mattbrailsford`

#### Fallback
By default when checking sources we will look for exact matches, but where there isn't an exact match, we will also compare the sources list against the media items URL to see if that URL starts with a given source URL. So if you don't know the source URL, but you know all posts for your account will be on a consistent URL like `https://mydomain.com/blog/article-title` then you can add a source for `https://mydomain.com/blog` to capture all articles posted on that URL.

## `topics.json`

The `topics.json` file allows creating topic specific pages made up of articles tagged with connected tags. We can think of these as "super tags" allowing to currate a number of connected tags into a single topic.

To add a topic by submitting a PR with an update to `topics.json` file adding a topics entry to the root array. Topics should be added in alphabetical order by alias so please insert your data in the appropriate location.

The properties of the topics object are as follows:

| Property | Description |
| -- | -- |
| `alias` | A URL safe, all lowercase alias for your profile. This is used to constuct your profile URL in the format `https://umb.fyi/topic/{alias}`. Please make sure your alias is unique. |
| `name` | The display name for the topic. |
| `description` | A short description for the topic. |
| `url` | An optional URL to link to for more information. |
| `tags` | An array of tags that make up this topic. |