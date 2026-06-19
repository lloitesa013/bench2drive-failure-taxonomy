# Multi-seed closed-loop variance (expert, structural-cluster routes)

Routes: 18 | seeds/route: up to 3 | overall mean per-route DS std: **3.97**
Routes that flip pass(DS=100)<->fail across seeds: **3**; routes stable-clean across all seeds: **9**.

| route | scenario | n | mean DS | min | max | SD | flips? | per-seed DS |
|---|---|---|---|---|---|---|---|---|
| 2127 | OppositeVehicleTakingPri | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 2201 | EnterActorFlow | 3 | 86.7 | 60 | 100 | 18.9 | YES | 100/100/60 |
| 2790 | InvadingTurn | 3 | 95.7 | 96 | 96 | 0.0 | - | 96/96/96 |
| 2913 | OppositeVehicleTakingPri | 3 | 12.0 | 0 | 36 | 17.0 | var | 36/0/0 |
| 3564 | InvadingTurn | 1 | 14.0 | 14 | 14 | 0.0 | - | 14 |
| 3697 | OppositeVehicleTakingPri | 1 | 100.0 | 100 | 100 | 0.0 | - | 100 |
| 11755 | EnterActorFlow | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 23695 | InterurbanAdvancedActorF | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 23910 | InterurbanActorFlow | 3 | 76.7 | 65 | 100 | 16.5 | YES | 65/65/100 |
| 24078 | InterurbanAdvancedActorF | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 24098 | InterurbanActorFlow | 3 | 65.0 | 65 | 65 | 0.0 | - | 65/65/65 |
| 26401 | MergerIntoSlowTrafficV2 | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 26956 | SignalizedJunctionRightT | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
| 27018 | SignalizedJunctionRightT | 3 | 30.0 | 30 | 30 | 0.3 | var | 30/30/30 |
| 28087 | NonSignalizedJunctionLef | 3 | 86.7 | 60 | 100 | 18.9 | YES | 100/60/100 |
| 28093 | NonSignalizedJunctionLef | 1 | 100.0 | 100 | 100 | 0.0 | - | 100 |
| 28099 | SignalizedJunctionLeftTu | 2 | 60.0 | 60 | 60 | 0.0 | - | 60/60 |
| 28330 | SignalizedJunctionLeftTu | 3 | 100.0 | 100 | 100 | 0.0 | - | 100/100/100 |
