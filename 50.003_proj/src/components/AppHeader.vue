<template>
    <div>
        <v-container>
            <v-navigation-drawer
                fixed
                :clipped="$vuetify.breakpoint.mdAndUp"
                app
                v-model="drawerIsOpen"
                >
                <v-list dense v-for="item in drawerItems" :key="item.text">
                    
                    <v-list-tile @click="">
                        <v-list-tile-action>
                        <v-icon>{{ item.icon }}</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                        <v-list-tile-title>
                            <a :href="'/'+item.link">
                                {{ item.text }}
                            </a>
                        </v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>

                </v-list>
                </v-navigation-drawer>
                <v-toolbar
                    color="blue darken-3"   
                    dark
                    app
                    :clipped-left="$vuetify.breakpoint.mdAndUp"    
                    fixed
                    >
                    <v-toolbar-title style="width: 300px">
                        <v-toolbar-side-icon @click.stop="drawerIsOpen = !drawerIsOpen"></v-toolbar-side-icon>
                        <span class="hidden-sm-and-down">SUTD Calendar</span>
                    </v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn icon>
                        <v-icon large>notifications</v-icon>
                    </v-btn>
                    <v-btn icon>
                        <v-icon large>account_circle</v-icon>
                    </v-btn>
                </v-toolbar>
        </v-container>
    </div>
</template>

<script>
export default {
  name: 'AppHeader',
  data: () => ({
      drawerIsOpen: false,
      drawerItems: [
        { icon: 'contacts', text: 'Contacts', link: ''},
        { icon: 'assignment', text: 'Form Submission' , link: 'forms.html'},
        { icon: 'import_export', text: 'Export Calendar', link: ''},
        { icon: 'calendar_today', text: 'Calendar', link: ''},
        { icon: 'settings', text: 'Settings', link: '' },
        { icon: 'message', text: 'Messages', link: '' },
        { icon: 'help', text: 'Help', link: '' }
      ]
    }),
  })
}
</script>