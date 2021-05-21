import auth from './auth.module'
import universityStructure from './universityStructure.module'
import bypassSheet from './bypassSheet.module'
import bypassSheetSchema from './bypassSheetSchema.module'
import users from './users.module'
import role from './role.module'

export default {
	modules: {
		auth,
    universityStructure,
    bypassSheet,
    bypassSheetSchema,
    users,
    role,
	}
}
