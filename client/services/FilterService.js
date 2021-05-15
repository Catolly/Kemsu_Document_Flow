const FilterService = () => ({
  filterList: [],

  create(filter) {
    this.filterList.push({
      value: '', //selected
      name: filter.name, // placeholder
      postfix: filter.postfix || '',
      data: filter.data,
      options: filter.data,
      subscriptions: [],
      filteringPropName: filter.filteringPropName, //свойство, по которому будут фильтроваться пользователи
    })
  },

  get(name) {
    return this.filterList.find(filter => filter.name === name)
  },

  // Устанавливает новое значение фильтра и фильтрует options по subscriptions
  set(name, value) {
    const filter = this.get(name)
    filter.value = value
    this.filterAll()

    if (filter.subscriptions.length) {
      const currentOption = filter.options.find(option => option.value === value)
      filter.subscriptions.forEach(subscription => {
        if (!subscription.target.value)
          this.set(subscription.target.name, currentOption[subscription.propName])
      })
      this.filterAll()
    }

    this.filterList.forEach(filter => {
      if (filter.subscriptions.length) {
        const subscriberCurrentOption = filter.options.find(option => option.value === filter.value)
        if (!subscriberCurrentOption)
          filter.value = ''
      }
    })
  },

  // Подписывает фильтр subscriber на изменения options фильтра target
  subscribe(subscriberName, targetName, subscriberPropName) {
    const subscriber = this.get(subscriberName)
    const target = this.get(targetName)

    subscriber.subscriptions.push({
      target,
      propName: subscriberPropName, // свойство, по которому будет фильтроваться subscriber
    })
  },

  // фильтрует filter options по subscriptions value
  filterOptions(filter) {
    if (!filter.subscriptions.length) {
      filter.options = filter.data
      return
    }

    filter.options = filter.data.filter(option =>
      filter.subscriptions.every(subscription =>
        !subscription.target.value
        || (subscription.target.value === option[subscription.propName])
      )
    )
  },

  // фильтрует options всех фильтров
  filterAll() {
    this.filterList.forEach(filter => {
      this.filterOptions(filter)
    })
  },

  // фильтрует options всех фильтров
  clear() {
    this.filterList.forEach(filter => {
      filter.value = ''
      filter.options = filter.data
    })
  },
})

export default FilterService

// Создает фильтр со структурой "институт"-"курс"-"группа"
export const initFilterService = groupsData => {
  const filterService = FilterService()

  // институты
  const institutes = groupsData
  .map(group => ({
    value: group.institute,
  }))
  .filter(group => group.value)

  // курсы
  const courseNumbers = groupsData
  .map(group => ({
    value: group.courseNumber,
  }))
  .filter(group => group.value)

  // группы
  const groups = groupsData.map(group => ({
    value: group.name,
    institute: group.institute,
    courseNumber: group.courseNumber,
  }))
  .filter(group => group.value)

  // создание фильтров
  if (institutes.length)
    filterService.create({
      name: 'Институт',
      data: institutes,
      filteringPropName: 'institute'
    })
  if (courseNumbers.length)
    filterService.create({
      name: 'Курс',
      postfix: ' курс',
      data: courseNumbers,
      filteringPropName: 'courseNumber'
    })
  if (groupsData.length) {
    filterService.create({
      name: 'Группа',
      data: groups,
      filteringPropName: 'group'
    })

    // подписка на обновления фильтров института и курса
    if (institutes.length)
      filterService.subscribe('Группа', 'Институт', 'institute')
    if (courseNumbers.length)
      filterService.subscribe('Группа', 'Курс', 'courseNumber')
  }

  return filterService
}
