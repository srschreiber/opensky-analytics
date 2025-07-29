# opensky-analytics
Perform flight analytics on opensky API: https://openskynetwork.github.io/opensky-api/

It combines Kafka and Apache Flink for analytics

Architecture:

[OpenSky API]
     ↓
[Amazon MSK]
     ↓
[Flink Job (KDA)]
     ↓
[WebSocket API service]
     ↓
[Browser/Web App]
