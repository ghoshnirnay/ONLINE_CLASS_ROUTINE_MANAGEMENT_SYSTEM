export default (context, inject) => {
  const base = context.$config.API_BASE || 'http://127.0.0.1:5000/api';

  const api = {

    // ------- Health Check -------
    async health() {
      const r = await fetch(base + '/health');
      return r.json();
    },

    // ------- Auth -------
    async login(email, password) {
      const r = await fetch(base + '/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      return r.json();
    },

    async register({ name, email, password, role }) {
      const r = await fetch(base + '/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role })
      });
      return r.json();
    },

    // ------- Departments -------
    async departments() {
      const r = await fetch(base + '/departments');
      return r.json();
    },

    async addDepartment(name) {
      const r = await fetch(base + '/departments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      });
      return r.json();
    },

    // ------- Routines -------
    async routines(params = {}) {
      const qs = new URLSearchParams(params).toString();
      const r = await fetch(base + '/routines' + (qs ? ('?' + qs) : ''));
      return r.json();
    },

    async addRoutine(payload) {
      const r = await fetch(base + '/routines', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      return r.json();
    },

    async updateRoutine(id, changes) {
      const r = await fetch(base + '/routines/' + id, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(changes)
      });
      return r.json();
    },

    async deleteRoutine(id) {
      const r = await fetch(base + '/routines/' + id, { method: 'DELETE' });
      return r.json();
    },

    // ------- Subjects -------
    async subjects() {
      return (await fetch(base + "/subjects")).json();
    },

    async addSubject(name) {
      return (await fetch(base + "/subjects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      })).json();
    },

    async deleteSubject(id) {
      return (await fetch(base + "/subjects/" + id, { method: "DELETE" })).json();
    },

    // ------- Faculty - Subjects -------
    async facultySubjects(facultyId) {
      return (await fetch(base + `/faculty-subjects/${facultyId}`)).json();
    },

    async assignFacultySubject(faculty_id, subject_id) {
      return (await fetch(base + `/faculty-subjects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ faculty_id, subject_id })
      })).json();
    },

    async removeFacultySubject(id) {
      return (await fetch(base + `/faculty-subjects/${id}`, { method: "DELETE" })).json();
    },

    // ------- Rooms -------
    async rooms() {
      const r = await fetch(base + '/rooms');
      return r.json();
    },

    async addRoom(name, capacity) {
      const r = await fetch(base + '/rooms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, capacity })
      });
      return r.json();
    },

    async deleteRoom(id) {
      const r = await fetch(base + '/rooms/' + id, { method: 'DELETE' });
      return r.json();
    },

    // ------- Time Slots -------
    async timeSlots() {
      const r = await fetch(base + '/time-slots');
      return r.json();
    },

    async addTimeSlot(label, start, end) {
      const r = await fetch(base + '/time-slots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ label, start_time: start, end_time: end })
      });
      return r.json();
    },

    async deleteTimeSlot(id) {
      const r = await fetch(base + '/time-slots/' + id, { method: 'DELETE' });
      return r.json();
    },

  };

  inject('api', api);
  context.$api = api;
};
