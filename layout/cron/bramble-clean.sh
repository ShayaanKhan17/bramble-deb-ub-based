#!/bin/bash
# =================================================================
# BrambleOS Automated Snapshot Retention Engine
# Runs Daily via /etc/cron.daily/
# Keeps Timeshift storage footprint capped at a target threshold.
# =================================================================

# --- CONFIGURATION INITIALIZATION ---
# Max percentage of total disk space allowed for system snapshots (Default: 5%)
MAX_PERCENT_QUOTA=5

# Fetch the root storage device utilization metrics dynamically
TOTAL_DISK_SIZE_KB=$(df / | awk 'NR==2 {print $2}')
USED_DISK_SPACE_KB=$(df / | awk 'NR==2 {print $3}')

# Calculate the actual byte block allowance limit for backup snapshots
SNAPSHOT_ALLOWANCE_KB=$((TOTAL_DISK_SIZE_SIZE_KB * MAX_PERCENT_QUOTA / 100))

# Locate the actual footprint block allocation size of the Timeshift directories
# Timeshift defaults to /timeshift/snapshots/ on standard file systems
TIMESHIFT_DIR="/timeshift/snapshots"

echo "⏳ BrambleOS Storage Monitor: Analyzing environment data layers..."

if [ ! -d "$TIMESHIFT_DIR" ]; then
    echo "✔️ No snapshot tree detected. Storage layers clean."
    exit 0
fi

# Calculate the actual current weight of all system save states combined
CURRENT_SNAPSHOT_USAGE_KB=$(du -s "$TIMESHIFT_DIR" | awk '{print $1}')
USAGE_PERCENT=$((CURRENT_SNAPSHOT_USAGE_KB * 100 / TOTAL_DISK_SIZE_KB))

echo "📊 Snapshot Storage footprint: ${USAGE_PERCENT}% of disk allocation limit."

# --- SMART PRUNING LAYER LOOP ---
# Loop and destroy the oldest snapshot files if usage breaks past our threshold
while [ "$CURRENT_SNAPSHOT_USAGE_KB" -gt "$SNAPSHOT_ALLOWANCE_KB" ]; do
    # Query the oldest snapshot directory name by sorting chronological folder layers
    OLDEST_SNAPSHOT=$(ls -1rt "$TIMESHIFT_DIR" | head -n 1)
    
    if [ -z "$OLDEST_SNAPSHOT" ]; then
        echo "⚠️ Target snapshot index exhausted but quota limit remains breached."
        break
    fi
    
    echo "🚨 Storage quota exceeded ($MAX_PERCENT_QUOTA%)! Purging oldest state asset: $OLDEST_SNAPSHOT"
    
    # Safely invoke the native timeshift command array to execute an orderly block removal
    timeshift --delete --snapshot "$OLDEST_SNAPSHOT" --script-mode
    
    # Re-calculate usage footprint weights before shifting back up through the loop validation
    CURRENT_SNAPSHOT_USAGE_KB=$(du -s "$TIMESHIFT_DIR" | awk '{print $1}')
done

echo "✔️ Retention enforcement sequence finalized perfectly."