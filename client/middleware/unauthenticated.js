import { CHECK_AUTH } from '~/store/actions.type'

export default async function ({ store, redirect }) {
  await store.dispatch(CHECK_AUTH)
  if (store.state.auth.isAuthenticated)
    return redirect('/')
}
