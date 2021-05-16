import auth from './auth.module'
import universityStructure from './universityStructure.module'
import bypassSheet from './bypassSheet.module'
import bypassSheetShema from './bypassSheetShema.module'
import users from './users.module'
import role from './role.module'

export default {
	modules: {
		auth,
    universityStructure,
    bypassSheet,
    bypassSheetShema,
    users,
    role,
	}
}
