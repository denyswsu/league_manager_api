# Chat app that uses Centrifugo
WebSocket connection here is mono-directional, e.g. we send ws message to clients
via Centrifugo HTTP broadcast API (like push notifications).
Front-end sends chat messages via DRF HTTP API directly.

![image](https://github.com/marzique/league_manager_api/assets/70688819/d898f43b-8a65-4f00-b4f2-454771dd0f15)
