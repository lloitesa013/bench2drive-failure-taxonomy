# Structural-cluster forensics — why the privileged expert also fails

For the interactive-traffic scenario classes where the calibration flags a structural ceiling,
we list every route on which **either** agent fails (DS < 100), with each agent's status and the
non-zero infraction signature. Source: `per_route/<id>/checkpoint_endpoint.json` (model) and
`expert/per_route/<id>/endpoint.json` (expert).

Key reading: the expert's failures here are **collisions** (vehicle during right-of-way
negotiation; layout while threading actor-flow / invading-turn geometry), not timidity. Within a
class the two agents often fail *different* instances — so the **class**, not a single route, is the
structural ceiling.

| scenario | route | model DS / status / infractions | expert DS / status / infractions |
|---|---|---|---|
| EnterActorFlow | 2201 | 42.0 Completed / collisions_vehicle:1, red_light:1 | 100.0 Completed / min_speed |
| EnterActorFlow | 11755 | 29.6 Failed-AgentDev / collisions_vehicle:1, min_speed | 100.0 Completed / min_speed |
| InterurbanActorFlow | 23910 | 96.1 Failed-AgentDev / min_speed, route_dev:1 | **17.7 Failed-Blocked / collisions_layout:1, min_speed** |
| InterurbanActorFlow | 24098 | 96.1 Failed-AgentDev / min_speed, route_dev:1 | **65.0 Completed / collisions_layout:1, min_speed** |
| InterurbanAdvancedActorFlow | 23695 | 60.0 Completed / collisions_vehicle:1 | 100.0 Completed / min_speed |
| InterurbanAdvancedActorFlow | 24078 | 60.0 Completed / collisions_vehicle:1 | 100.0 Completed / min_speed |
| InvadingTurn | 2790 | 99.0 Completed / outside_route_lanes:1 | 97.0 Completed / outside_route_lanes:1 |
| InvadingTurn | 3564 | 100.0 Completed / min_speed | **14.0 Failed-TickRuntime / collisions_layout:3** |
| MergerIntoSlowTrafficV2 | 26401 | 60.0 Completed / collisions_vehicle:1 | 100.0 Completed / min_speed |
| NonSignalizedJunctionLeftTurnEnterFlow | 28087 | 100.0 Completed / min_speed | **60.0 Completed / collisions_vehicle:1** |
| NonSignalizedJunctionLeftTurnEnterFlow | 28093 | 30.9 Failed-TickRuntime / min_speed | 100.0 Completed / min_speed |
| OppositeVehicleTakingPriority | 2127 | 60.0 Completed / collisions_vehicle:1 | 100.0 Completed / min_speed |
| OppositeVehicleTakingPriority | 2913 | 100.0 Completed / min_speed | **60.0 Completed / collisions_vehicle:1** |
| OppositeVehicleTakingPriority | 3697 | 100.0 Completed / min_speed | **65.0 Completed / collisions_layout:1** |
| SignalizedJunctionLeftTurnEnterFlow | 28099 | 100.0 Completed / min_speed | **32.5 Failed-TickRuntime / collisions_vehicle:1** |
| SignalizedJunctionLeftTurnEnterFlow | 28330 | 60.0 Completed / collisions_vehicle:1 | 100.0 Completed / min_speed |
| SignalizedJunctionRightTurn | 26956 | (model crashed: NOREC) | 100.0 Completed / min_speed  *(a\*)* |
| SignalizedJunctionRightTurn | 26966 | (model crashed: NOREC) | (expert crashed: NOREC)  *(a)* |
| SignalizedJunctionRightTurn | 27018 | 60.0 Completed / collisions_vehicle:1 | **30.2 Failed-TickRuntime / collisions_vehicle:1** |

**Summary of the expert's failure modes (structural cluster):** layout collisions on
InterurbanActorFlow / InvadingTurn geometry (worst DS 14–18), and vehicle collisions during
junction right-of-way negotiation (DS 30–65). The same collision class that defeats the
sensorimotor model defeats the privileged planner — evidence that these are scenario-level
structural ceilings, not perception gaps.
