import { CHECK_AUTH } from '~/store/actions.type'

export default async function ({ store, redirect }) {
  if (process.browser) {
    await store.dispatch(CHECK_AUTH)
    if (store.state.auth.isAuthenticated)
      return redirect('/')
  }
}
