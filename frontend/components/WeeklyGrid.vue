<template>
  <div class="timetable card">
    <table class="table">
      <thead>
        <tr>
          <th>Time</th>
          <th v-for="day in days" :key="day">{{ day }}</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="slot in timeSlots" :key="slot">
          <td class="time-col">{{ slot }}</td>

          <td v-for="day in days" :key="day">
            <div v-if="cell(day, slot)" class="class-box">
              <strong>{{ cell(day, slot).subject }}</strong><br>
              {{ cell(day, slot).room }}<br>
              <small>{{ cell(day, slot).start_time }} - {{ cell(day, slot).end_time }}</small>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ["routines"],
  data() {
    return {
      days: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      timeSlots: [
        "09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00"
      ]
    };
  },
  methods: {
    cell(day, time) {
      return this.routines.find(r => r.day === day && r.start_time === time);
    }
  }
};
</script>

<style scoped>
.time-col {
  font-weight: bold;
  width: 90px;
}
.class-box {
  padding: 6px;
  background: #e8f5ff;
  border: 1px solid #b7d9f7;
  border-radius: 4px;
  text-align: center;
  font-size: 13px;
}
</style>
