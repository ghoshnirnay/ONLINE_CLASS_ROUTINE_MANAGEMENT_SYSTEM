export default function ({ store, route, redirect }) {
  // Get user from Vuex OR localStorage fallback
  const user = store.state.user || JSON.parse(localStorage.getItem("user") || "null")

  // If not logged in and trying to access a protected page → redirect
  // Allow unauthenticated access to the landing page ('/') as well as login/register
  if (!user && route.path !== '/login' && route.path !== '/register' && route.path !== '/') {
    return redirect('/login')
  }
}
