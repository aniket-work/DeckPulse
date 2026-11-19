# Eventhouse create and ingest for DeckPulse

This PoC mirrors a laptop CSV into a Microsoft Fabric Eventhouse so the same
parking-garage gate readings can be queried with KQL. The steps below match the
names used in the README.

## Prerequisites

1. A Microsoft Fabric workspace on a Fabric-enabled capacity
2. Permission to create items in that workspace
3. The sample file `data/gate_telemetry.csv` (or regenerate it with
   `python data/generate_gate_telemetry.py`)

## Create the Eventhouse

1. Open the workspace.
2. Select **New item**.
3. Under **Track data**, select **Eventhouse**.
4. Name it `DeckPulseEventhouse` and select **Create**.
5. Dismiss the welcome dialog when it appears.

Fabric also creates a default KQL database with the same name and a default
queryset (`DeckPulseEventhouse_queryset`).

## Ingest the local CSV

1. Open the `DeckPulseEventhouse` KQL database.
2. Select **Get data**, then **Local file**.
3. Select **+ New table** and name it `GateReadings`.
4. Upload `data/gate_telemetry.csv` and select **Next**.
5. On the **Inspect** step:
   - Format: **CSV**
   - Turn on **First row header**
   - Keep the auto-created mapping (`GateReadings_mapping`)
6. Select **Finish** and wait for create table, create mapping, and data
   queuing to succeed.

You should see about **6,000 rows** in the Data Activity Tracker.

## Explore with KQL

Open the default queryset and run the statements in `kql/01_explore.kql` one
at a time. Clear any placeholder sample text first. The laptop brief from
`python main.py` is designed to agree with those queries on row count, deck
averages, and ALERT totals.

## Notes I kept for myself

1. An Eventhouse is the container. The KQL database is where tables live.
2. Local-file ingest is a one-shot path. Continuous options such as Eventstream
   or Event Hubs are a later experiment.
3. OneLake availability can later expose the same table as Delta. This PoC
   leaves it off.
4. Compute can pause when idle. The first query after a pause may take a few
   seconds to wake the Eventhouse.
