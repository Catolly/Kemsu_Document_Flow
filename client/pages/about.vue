<template>
  <div class="about">
    <h1 class="header">О проекте</h1>

    <h3 class="description">
      Проект выполнен в рамках дипломной работы с целью упростить процесс прохождения обходного листа и перенести его в дистанционный формат
    </h3>

    <div class="creators">
      <div v-for="(creator, index) in creators" :key="index" class="creator">
        <span class="role">{{creator.role}}</span>
        <h2 class="name">{{creator.name}}</h2>
        <template v-for="(link, index) in creator.links">
          <a
            :key="index"
            :href="link.path"
            target="_blank"
            class="link clear"
          >
            <span class="line" />{{link.name}}
          </a>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'about',

  middleware: 'authenticated',

  data:() => ({
    creators: [
      {
        name: 'Бурмин Леонид',
        role: 'Научный руководитель',
      },
      {
        name: 'Сергиенко Анатолий',
        role: 'Frontend-разработчик',
        links: [
          {
            name: 'Github',
            path: 'https://github.com/Catolly',
          },
        ],
      },
      {
        name: 'Люкшин Михаил',
        role: 'Backend-разработчик',
        links: [
          {
            name: 'Github',
            path: 'https://github.com/gumart',
          },
        ],
      },
      {
        name: 'Панчук Роман',
        role: 'Backend-разработчик',
        links: [
          {
            name: 'Github',
            path: 'https://github.com/PanchukRoman',
          },
        ],
      },
      {
        name: 'Козырева Татьяна',
        role: 'Дизайнер',
      },
      {
        name: 'Колчанов Дмитрий',
        role: 'Тестировщик',
      },
      {
        name: 'Игор Миронов',
        role: 'Тестировщик',
      },
    ],
  }),
}
</script>

<style scoped lang="less">
.about {
  padding-top: 48px;

  display: flex;
  flex-direction: column;
  gap: 3em;
}

.description {
  max-width: 750px;
}

.creators {
  max-width: 1000px;
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-column-gap: 1em;
  grid-row-gap: 2em;
}

.creator {
  display: flex;
  flex-direction: column;
  gap: .5em;

  &:first-child {
    grid-column: 1 / -1;
  }
}

.role {
  font-size: @fz-small;
  color: @grey-darkset;
}

.link {
  width: fit-content;
  font-size: @fz-large;
  font-weight: @fw-normal;
  color: @black;

  display: flex;
  align-items: center;
}

.line {
  margin-right: .5em;

  display: inline-block;
  width: 1em;

  position: relative;
  &:before {
    .absolute();
    top: 50%;
    height: 1px;
    width: 100%;
    background: @grey-darkset;
  }
}
</style>
