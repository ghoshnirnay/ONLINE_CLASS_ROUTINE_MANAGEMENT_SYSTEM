import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from 'ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _06d9f42e = () => interopDefault(import('..\\pages\\dashboard.vue' /* webpackChunkName: "pages/dashboard" */))
const _71ee7ebe = () => interopDefault(import('..\\pages\\login.vue' /* webpackChunkName: "pages/login" */))
const _3618b4a2 = () => interopDefault(import('..\\pages\\manage\\index.vue' /* webpackChunkName: "pages/manage/index" */))
const _89708086 = () => interopDefault(import('..\\pages\\notifications.vue' /* webpackChunkName: "pages/notifications" */))
const _1740395e = () => interopDefault(import('..\\pages\\register.vue' /* webpackChunkName: "pages/register" */))
const _57011cea = () => interopDefault(import('..\\pages\\routines.vue' /* webpackChunkName: "pages/routines" */))
const _7e12fc90 = () => interopDefault(import('..\\pages\\swap-request.vue' /* webpackChunkName: "pages/swap-request" */))
const _5e4eb84a = () => interopDefault(import('..\\pages\\admin\\swap-requests.vue' /* webpackChunkName: "pages/admin/swap-requests" */))
const _c623a120 = () => interopDefault(import('..\\pages\\manage\\faculty-subjects.vue' /* webpackChunkName: "pages/manage/faculty-subjects" */))
const _27a6a3c8 = () => interopDefault(import('..\\pages\\manage\\rooms.vue' /* webpackChunkName: "pages/manage/rooms" */))
const _49602ab2 = () => interopDefault(import('..\\pages\\manage\\subjects.vue' /* webpackChunkName: "pages/manage/subjects" */))
const _dcea36e4 = () => interopDefault(import('..\\pages\\manage\\swap-requests.vue' /* webpackChunkName: "pages/manage/swap-requests" */))
const _c0be5fd6 = () => interopDefault(import('..\\pages\\manage\\time-slots.vue' /* webpackChunkName: "pages/manage/time-slots" */))
const _06b934ea = () => interopDefault(import('..\\pages\\manage\\routines\\create.vue' /* webpackChunkName: "pages/manage/routines/create" */))
const _af7248b2 = () => interopDefault(import('..\\pages\\index.vue' /* webpackChunkName: "pages/index" */))

const emptyFn = () => {}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/dashboard",
    component: _06d9f42e,
    name: "dashboard"
  }, {
    path: "/login",
    component: _71ee7ebe,
    name: "login"
  }, {
    path: "/manage",
    component: _3618b4a2,
    name: "manage"
  }, {
    path: "/notifications",
    component: _89708086,
    name: "notifications"
  }, {
    path: "/register",
    component: _1740395e,
    name: "register"
  }, {
    path: "/routines",
    component: _57011cea,
    name: "routines"
  }, {
    path: "/swap-request",
    component: _7e12fc90,
    name: "swap-request"
  }, {
    path: "/admin/swap-requests",
    component: _5e4eb84a,
    name: "admin-swap-requests"
  }, {
    path: "/manage/faculty-subjects",
    component: _c623a120,
    name: "manage-faculty-subjects"
  }, {
    path: "/manage/rooms",
    component: _27a6a3c8,
    name: "manage-rooms"
  }, {
    path: "/manage/subjects",
    component: _49602ab2,
    name: "manage-subjects"
  }, {
    path: "/manage/swap-requests",
    component: _dcea36e4,
    name: "manage-swap-requests"
  }, {
    path: "/manage/time-slots",
    component: _c0be5fd6,
    name: "manage-time-slots"
  }, {
    path: "/manage/routines/create",
    component: _06b934ea,
    name: "manage-routines-create"
  }, {
    path: "/",
    component: _af7248b2,
    name: "index"
  }],

  fallback: false
}

export function createRouter (ssrContext, config) {
  const base = (config._app && config._app.basePath) || routerOptions.base
  const router = new Router({ ...routerOptions, base  })

  // TODO: remove in Nuxt 3
  const originalPush = router.push
  router.push = function push (location, onComplete = emptyFn, onAbort) {
    return originalPush.call(this, location, onComplete, onAbort)
  }

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    return resolve(to, current, append)
  }

  return router
}
