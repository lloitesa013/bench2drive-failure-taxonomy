# Per-scenario model-vs-expert calibration — Bench2Drive-220 (44 classes x 5)

Expert coverage so far: 220/220 routes scored.

| scenario | model pass | model meanDS | model crash | expert pass | expert meanDS | expert crash | verdict |
|---|---|---|---|---|---|---|---|
| YieldToEmergencyVehicle | 0/4 | 70 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| HazardAtSideLaneTwoWays | 2/3 | 74 | 2 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| SignalizedJunctionRightTurn | 2/3 | 87 | 2 | 3/4 | 83 | 1 | (a) shared infra (both crash some) |
| ParkingExit | 3/3 | 100 | 2 | 3/3 | 100 | 2 | (a) shared infra (both crash some) |
| BlockedIntersection | 2/5 | 67 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| HighwayExit | 2/5 | 86 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| ParkingCrossingPedestrian | 3/4 | 88 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| SequentialLaneChange | 2/5 | 76 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| T_Junction | 3/4 | 92 | 1 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| Accident | 4/4 | 100 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| AccidentTwoWays | 4/4 | 100 | 1 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| EnterActorFlow | 3/5 | 74 | 0 | 4/5 | 93 | 0 | (c) structural: expert ALSO fails some |
| HardBreakRoute | 4/4 | 100 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| HazardAtSideLane | 4/4 | 100 | 1 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| InterurbanActorFlow | 3/5 | 98 | 0 | 3/5 | 77 | 0 | (c) structural: expert ALSO fails some |
| InterurbanAdvancedActorFlow | 3/5 | 84 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| NonSignalizedJunctionLeftTurn | 4/4 | 100 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| OppositeVehicleRunningRedLight | 4/4 | 100 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| ParkedObstacleTwoWays | 4/4 | 100 | 1 | 3/4 | 84 | 1 | (a) shared infra (both crash some) |
| ParkingCutIn | 4/4 | 100 | 1 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| PedestrianCrossing | 4/4 | 100 | 1 | 4/4 | 100 | 1 | (a) shared infra (both crash some) |
| CrossingBicycleFlow | 4/5 | 92 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| DynamicObjectCrossing | 4/5 | 90 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| InvadingTurn | 4/5 | 100 | 0 | 3/5 | 82 | 0 | (c) structural: expert ALSO fails some |
| MergerIntoSlowTrafficV2 | 4/5 | 92 | 0 | 3/5 | 99 | 0 | (c) structural: expert ALSO fails some |
| NonSignalizedJunctionLeftTurnEnterFlow | 4/5 | 86 | 0 | 4/5 | 92 | 0 | (c) structural: expert ALSO fails some |
| NonSignalizedJunctionRightTurn | 4/5 | 84 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| OppositeVehicleTakingPriority | 4/5 | 92 | 0 | 3/5 | 85 | 0 | (c) structural: expert ALSO fails some |
| SignalizedJunctionLeftTurnEnterFlow | 4/5 | 92 | 0 | 4/5 | 87 | 0 | (c) structural: expert ALSO fails some |
| VanillaNonSignalizedTurnEncounterStopsign | 4/5 | 82 | 0 | 5/5 | 100 | 0 | (b) fixable: expert solves all it ran |
| ConstructionObstacle | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| ConstructionObstacleTwoWays | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| ControlLoss | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| HighwayCutIn | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| MergerIntoSlowTraffic | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| ParkedObstacle | 5/5 | 100 | 0 | 4/5 | 92 | 0 | model-clean |
| SignalizedJunctionLeftTurn | 5/5 | 100 | 0 | 4/5 | 85 | 0 | model-clean |
| StaticCutIn | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| VanillaNonSignalizedTurn | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| VanillaSignalizedTurnEncounterGreenLight | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| VanillaSignalizedTurnEncounterRedLight | 5/5 | 100 | 0 | 2/5 | 82 | 0 | model-clean |
| VehicleOpensDoorTwoWays | 5/5 | 100 | 0 | 3/5 | 76 | 0 | model-clean |
| VehicleTurningRoute | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
| VehicleTurningRoutePedestrian | 5/5 | 100 | 0 | 5/5 | 100 | 0 | model-clean |
