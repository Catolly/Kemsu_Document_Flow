export const optionExist = (value, vm) => {
  return !!vm.relevantUsersOptionList.filter(option => option.value === value).length
}

export const twoOrThreeWordsReg = /^[а-яА-Я]+\s[а-яА-Я]+\s?[а-яА-Я]*$/ // От 2 до 3 слов
