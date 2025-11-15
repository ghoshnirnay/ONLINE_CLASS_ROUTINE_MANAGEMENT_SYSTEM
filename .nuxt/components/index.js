export { default as AdminDashboard } from '../..\\components\\AdminDashboard.vue'
export { default as FacultyDashboard } from '../..\\components\\FacultyDashboard.vue'
export { default as Header } from '../..\\components\\Header.vue'
export { default as Logo } from '../..\\components\\Logo.vue'
export { default as StudentDashboard } from '../..\\components\\StudentDashboard.vue'
export { default as WeeklyGrid } from '../..\\components\\WeeklyGrid.vue'
export { default as WeeklySchedule } from '../..\\components\\WeeklySchedule.vue'

// nuxt/nuxt.js#8607
function wrapFunctional(options) {
  if (!options || !options.functional) {
    return options
  }

  const propKeys = Array.isArray(options.props) ? options.props : Object.keys(options.props || {})

  return {
    render(h) {
      const attrs = {}
      const props = {}

      for (const key in this.$attrs) {
        if (propKeys.includes(key)) {
          props[key] = this.$attrs[key]
        } else {
          attrs[key] = this.$attrs[key]
        }
      }

      return h(options, {
        on: this.$listeners,
        attrs,
        props,
        scopedSlots: this.$scopedSlots,
      }, this.$slots.default)
    }
  }
}
