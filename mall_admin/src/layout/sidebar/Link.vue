<template>
  <component 
    :is="type" 
    v-bind="linkProps" 
    @click="handleClick"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { isExternal } from '@/utils/validate'

const router = useRouter()

const props = defineProps({
  to: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['click'])

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

// 处理点击事件
const handleClick = (e) => {
  console.log('Link组件点击:', props.to)
  
  if (isExternal(props.to)) {
    // 外部链接，保持默认行为
  } else {
    // 内部链接，触发click事件供父组件处理
    emit('click', e)
  }
}
</script>

<style scoped>
/* 确保链接样式正常 */
a {
  text-decoration: none;
  color: inherit;
}
</style> 