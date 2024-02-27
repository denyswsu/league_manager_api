# Backend API for League Manager App

## Description
This is the backend API of the League Manager application.

It is a Multi-tenant RESTful API that provides ability to create websites for football leagues and manage them.

User can create his own leagues website on a subdomain of the main website and manage it.
Each league website has its own database and can be managed by the owner.
Owner can create teams, players, matches, different type of competitions, such as:
- League
- Cup
- Friendly matches
- etc.

Owner can also manage the website settings, such as:
- Logo
- Colors
- etc.

## TODO:
- [ ] Dockerize the project
- [ ] Add CI/CD
- [ ] Add tests
- [ ] Host the project on AWS
- [ ] Implement basic tenant creation MVP (multi-tenancy)
- [ ] Implement basic league management functionality
- [ ] Implement websocket functionality (e.g chat, live scores, etc.)

## Extra TODO:
- [ ] Team management functionality (admins manage their teams, add players, etc.)
- [ ] Fantasy League functionality
- [ ] Betting functionality
- [ ] Chat functionality (under each match, league, team, player, etc.)
- [ ] Follow functionality (follow leagues, teams, players, etc.)
- [ ] Voting functionality (e.g. for the best player of the match, etc.)
- [ ] Team of the week functionality
- [ ] Match of the week functionality