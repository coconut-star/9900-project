<template>
<li>
    <div class="tree-text" :class="{active: active}">
        <span v-if="isFolder" @click="toggle" class="tree-text__cntrl"> {{ open?'-':'+' }} </span>
        <input v-else type="checkbox" name="skill_checkbox" :idvalue="model.id" :namevalue="model.label">
        <!-- @click="nodeClick(model)" -->
        <span>{{ model.label }}</span>
    </div>
    <ul v-for="td in children" v-show="open">
        <tree-node :model="td"></tree-node>
    </ul>
</li>
</template>

<script>
import axios from 'axios'
export default {
    name: 'treeNode',
    props: ['model'],
    data() {
        return {
            open: false,
            active: false,
            children: []
        }
    },
    computed: {
        isFolder() {
            return this.model.type === "C";
        }
    },
    methods: {
        toggle() {
            if (this.isFolder) {
                if (this.children.length == 0) {
                    axios({
                        method: 'get',
                        url: API_HOST +'/api/skills/',
                        params: {
                            category: this.model.id
                        }
                    }).then(response => {
                        var skills = response.data
                        this.children = []
                        for (var index in skills) {
                            var skill = skills[index]
                            this.children.push({
                                label: skill.name,
                                type: skill.type,
                                id: skill.id
                            })
                        }
                    })
                }
                this.open = !this.open;
            }
        },
        nodeClick(model) {
            this.active = !this.active;
            if (this.active) {
                this.tree.$emit('nodeSelectedClick', model);
            }
        }
    },
    created() {
        const parent = this.$parent;
        if (parent.isTree) {
            this.tree = parent;
        } else {
            this.tree = parent.tree;
        }
    }
}
</script>

<style lang="scss">
.tree-text {
    .tree-text__cntrl {
        display: inline-block;
        width: 20px;
        text-align: center;
        cursor: pointer;
    }
}
</style>
<style>
ul {
  padding-left: 1em;
  line-height: 1.5em;
  list-style-type: dot;
}
</style>
