# LEAD tfv6 — Bench2Drive-220 Failure Taxonomy v0

Baseline: mean Driving Score **89.38** over 211 scored routes (single checkpoint `model_0030_0`; published 3-seed ensemble ref 95.28).

Failures classified: **50**  —  (a) integration/env: **22**  ·  (b) fixable logic: **28**  ·  (c) structural ceiling (candidate): **0**

> (c) is a *candidate* label only: it cannot be asserted from the learned model alone — it requires an expert (PDM-Lite / LEAD-expert) comparison to confirm a true benchmark ceiling.


## (a) Integration / env — 22 (re-run candidates, NOT driving failures)

| route | status | score |
| --- | --- | --- |
| 2204 | Failed - TickRuntime | 30.26 |
| 24206 | Failed - Simulation crashed | 0.0 |
| 24759 | Started | None |
| 24816 | Failed - Simulation crashed | 0.0 |
| 25378 | Started | None |
| 25381 | Started | None |
| 25854 | Failed - Simulation crashed | 0.0 |
| 25857 | Started | None |
| 25896 | Failed - Simulation crashed | 0.0 |
| 25955 | Started | None |
| 26393 | Started | None |
| 26435 | Failed - Simulation crashed | 0.0 |
| 26456 | Failed - Simulation crashed | 0.0 |
| 26950 | Failed - Simulation crashed | 0.0 |
| 26956 | Started | None |
| 26966 | Started | None |
| 26990 | Failed - Simulation crashed | 0.0 |
| 27515 | Failed - Simulation crashed | 0.0 |
| 28048 | Started | None |
| 28093 | Failed - TickRuntime | 30.86 |
| 2903 | Failed - TickRuntime | 21.132 |
| 2989 | Failed - TickRuntime | 32.56 |

## (b) Fixable model-policy errors — 28

Grouped by scenario type (systematic clusters first):

- **YieldToEmergencyVehicle** — 4 route(s): 3364(DS 70), 3373(DS 70), 3378(DS 70), 3380(DS 70)
- **SequentialLaneChange** — 3 route(s): 17563(DS 60), 17635(DS 60), 17655(DS 60)
- **HighwayExit** — 3 route(s): 23659(DS 80), 23687(DS 97), 24041(DS 56)
- **EnterActorFlow** — 2 route(s): 11755(DS 30), 2201(DS 42)
- **InterurbanAdvancedActorFlow** — 2 route(s): 23695(DS 60), 24078(DS 60)
- **InterurbanActorFlow** — 2 route(s): 23910(DS 96), 24098(DS 96)
- **ParkingCrossingPedestrian** — 1 route(s): 18252(DS 50)
- **OppositeVehicleTakingPriority** — 1 route(s): 2127(DS 60)
- **BlockedIntersection** — 1 route(s): 2215(DS 70)
- **DynamicObjectCrossing** — 1 route(s): 24224(DS 50)
- **MergerIntoSlowTrafficV2** — 1 route(s): 26401(DS 60)
- **SignalizedJunctionRightTurn** — 1 route(s): 27018(DS 60)
- **InvadingTurn** — 1 route(s): 2790(DS 99)
- **T_Junction** — 1 route(s): 28035(DS 70)
- **SignalizedJunctionLeftTurnEnterFlow** — 1 route(s): 28330(DS 60)
- **CrossingBicycleFlow** — 1 route(s): 3093(DS 60)
- **HazardAtSideLaneTwoWays** — 1 route(s): 3436(DS 22)
- **VanillaNonSignalizedTurnEncounterStopsign** — 1 route(s): 3905(DS 8)

| route | scenario | DS | infractions | hypothesis | conf |
| --- | --- | --- | --- | --- | --- |
| 3905 | VanillaNonSignalizedTurnEncounterStopsign_1 | 7.9 | min_speed_infractions:1, vehicle_blocked:1 | Model got blocked/stuck -- overly cautious or failed maneuver | med |
| 3436 | HazardAtSideLaneTwoWays_1 | 21.6 | collisions_vehicle:3, min_speed_infractions:18 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 11755 | EnterActorFlow_1 | 29.6 | collisions_vehicle:1, min_speed_infractions:8, route_dev:1 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 2201 | EnterActorFlow_1 | 42.0 | collisions_vehicle:1, min_speed_infractions:17, red_light:1 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 18252 | ParkingCrossingPedestrian_1 | 50.0 | collisions_pedestrian:1, min_speed_infractions:20 | Model struck a crossing pedestrian -- perception/braking gap (safety-critical) | high |
| 24224 | DynamicObjectCrossing_1 | 50.0 | collisions_pedestrian:1, min_speed_infractions:20 | Model struck a crossing pedestrian -- perception/braking gap (safety-critical) | high |
| 24041 | HighwayExit_1 | 55.6 | collisions_layout:1, min_speed_infractions:17, outside_route_lanes:1, vehicle_blocked:1 | Model hit static layout (curb/barrier) -- path/lateral control | med |
| 17563 | SequentialLaneChange_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:19 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 17635 | SequentialLaneChange_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:19 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 17655 | SequentialLaneChange_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:18 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 2127 | OppositeVehicleTakingPriority_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:20 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 23695 | InterurbanAdvancedActorFlow_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:20 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 24078 | InterurbanAdvancedActorFlow_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:20 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 26401 | MergerIntoSlowTrafficV2_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:18 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 27018 | SignalizedJunctionRightTurn_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:21 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 28330 | SignalizedJunctionLeftTurnEnterFlow_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:20 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 3093 | CrossingBicycleFlow_1 | 60.0 | collisions_vehicle:1, min_speed_infractions:18 | Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing | med |
| 2215 | BlockedIntersection_1 | 70.0 | min_speed_infractions:20, red_light:1 | Model ran a red light -- traffic-light compliance gap | high |
| 28035 | T_Junction_1 | 70.0 | min_speed_infractions:19, red_light:1 | Model ran a red light -- traffic-light compliance gap | high |
| 3364 | YieldToEmergencyVehicle_1 | 70.0 | min_speed_infractions:19, yield_emergency_vehicle_infractions:1 | Model fails to yield to emergency vehicle -- missing scenario behavior (systematic) | high |
| 3373 | YieldToEmergencyVehicle_1 | 70.0 | min_speed_infractions:19, yield_emergency_vehicle_infractions:1 | Model fails to yield to emergency vehicle -- missing scenario behavior (systematic) | high |
| 3378 | YieldToEmergencyVehicle_1 | 70.0 | min_speed_infractions:19, yield_emergency_vehicle_infractions:1 | Model fails to yield to emergency vehicle -- missing scenario behavior (systematic) | high |
| 3380 | YieldToEmergencyVehicle_1 | 70.0 | min_speed_infractions:18, yield_emergency_vehicle_infractions:1 | Model fails to yield to emergency vehicle -- missing scenario behavior (systematic) | high |
| 23659 | HighwayExit_1 | 79.9 | min_speed_infractions:12, route_dev:1 | Model deviated from route / left lane -- path-following/localization | med |
| 23910 | InterurbanActorFlow_1 | 96.1 | min_speed_infractions:18, route_dev:1 | Model deviated from route / left lane -- path-following/localization | med |
| 24098 | InterurbanActorFlow_1 | 96.1 | min_speed_infractions:18, route_dev:1 | Model deviated from route / left lane -- path-following/localization | med |
| 23687 | HighwayExit_1 | 96.8 | min_speed_infractions:20, outside_route_lanes:1 | Model deviated from route / left lane -- path-following/localization | med |
| 2790 | InvadingTurn_1 | 99.0 | min_speed_infractions:19, outside_route_lanes:1 | Model deviated from route / left lane -- path-following/localization | med |
