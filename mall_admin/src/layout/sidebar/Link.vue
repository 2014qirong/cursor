<template>
  <component 
    :is="type" 
    v-bind="linkProps"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { isExternal } from '@/utils/validate'

const props = defineProps({
  to: {
    type: String,
    required: true
  }
})

// 链接类型: 外部链接使用a标签，内部链接使用router-link
const type = computed(() => {
  return isExternal(props.to) ? 'a' : 'router-link'
})

// 链接属性: 外部链接设置href和target，内部链接设置to属性
const linkProps = computed(() => {
  if (isExternal(props.to)) {
    return {
      href: props.to,
      target: '_blank',
      rel: 'noopener'
    }
  }
  return {
    to: props.to
  }
})
</script>

<style scoped>
/* 确保链接样式正常 */
a {
  text-decoration: none;
  color: inherit;
}
</style> 