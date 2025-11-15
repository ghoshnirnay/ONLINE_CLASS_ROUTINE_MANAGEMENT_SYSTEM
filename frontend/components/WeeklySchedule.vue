<template>
  <div class="weekly-schedule">
    <div class="schedule-grid">
      <div class="day-column" v-for="day in days" :key="day.value">
        <div class="day-header" :class="{ today: isToday(day.value) }">
          <div class="day-name">{{ day.label }}</div>
          <div class="day-date">{{ getDateForDay(day.value) }}</div>
        </div>

        <div class="day-content">
          <div
            v-for="routine in getRoutinesForDay(day.value)"
            :key="routine.id"
            class="routine-card"
          >
            <div class="routine-time">
              {{ routine.time_slots?.start_time }} - {{ routine.time_slots?.end_time }}
            </div>
            <div class="routine-subject">{{ routine.subjects?.name }}</div>
            <div class="routine-details">
              <span v-if="routine.profiles">👨‍🏫 {{ routine.profiles.full_name }}</span>
              <span v-if="routine.rooms">🚪 {{ routine.rooms.name }}</span>
            </div>
          </div>

          <div v-if="getRoutinesForDay(day.value).length === 0" class="no-classes">
            No classes
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    routines: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      days: [
        { label: 'Monday', value: 1 },
        { label: 'Tuesday', value: 2 },
        { label: 'Wednesday', value: 3 },
        { label: 'Thursday', value: 4 },
        { label: 'Friday', value: 5 },
        { label: 'Saturday', value: 6 },
        { label: 'Sunday', value: 7 }
      ]
    }
  },
  methods: {
    getRoutinesForDay(dayValue) {
      return this.routines.filter(r => r.day_of_week === dayValue)
    },
    isToday(dayValue) {
      const today = new Date().getDay()
      return (today === 0 ? 7 : today) === dayValue
    },
    getDateForDay(dayValue) {
      const today = new Date()
      const currentDay = today.getDay() || 7
      const diff = dayValue - currentDay
      const targetDate = new Date(today)
      targetDate.setDate(today.getDate() + diff)
      return targetDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }
  }
}
</script>

<style scoped>
.weekly-schedule {
  overflow-x: auto;
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(180px, 1fr));
  gap: 1px;
  background: var(--gray-200);
  border: 1px solid var(--gray-200);
  border-radius: 0.5rem;
  overflow: hidden;
  min-width: 1260px;
}

.day-column {
  background: white;
  display: flex;
  flex-direction: column;
}

.day-header {
  padding: 1rem;
  background: var(--gray-50);
  border-bottom: 2px solid var(--gray-200);
  text-align: center;
}

.day-header.today {
  background: var(--primary);
  color: white;
}

.day-name {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.day-date {
  font-size: 0.75rem;
  opacity: 0.8;
}

.day-content {
  padding: 0.75rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.routine-card {
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-left: 3px solid var(--primary);
  border-radius: 0.375rem;
  padding: 0.75rem;
  transition: all 0.2s;
}

.routine-card:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.routine-time {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 0.375rem;
}

.routine-subject {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: 0.5rem;
}

.routine-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--gray-600);
}

.no-classes {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--gray-400);
  font-size: 0.875rem;
}

@media (max-width: 1280px) {
  .schedule-grid {
    grid-template-columns: repeat(7, 200px);
  }
}
</style>
