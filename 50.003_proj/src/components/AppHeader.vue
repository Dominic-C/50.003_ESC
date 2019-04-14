<template>
	<div>
		<v-navigation-drawer
			fixed
			:clipped="$vuetify.breakpoint.mdAndUp"
			app
			v-model="drawerIsOpen"
			>
			<v-list dense v-for="item in drawerItems" :key="item.text">
				<v-list-group v-if="item.children"
					v-model="item.open"
					:key="item.text"
					:prepend-icon="item.icon"
				>
					<v-list-tile slot="activator">
						<v-list-tile-content>
							<v-list-tile-title>
								{{ item.text }}
							</v-list-tile-title>
						</v-list-tile-content>
					</v-list-tile>
					<v-list-tile v-for="(child, i) in item.children"
						:key="i"
						@click="toggleVisible(child.name)"
					>
						<v-list-tile-content>
							<!-- <v-icon>
								{{ child.icon }}
							</v-icon> -->
							<v-list-tile-title >
								{{ child.text }}
							</v-list-tile-title>
						</v-list-tile-content>
					</v-list-tile>
				</v-list-group>

				<!-- for no subgroup -->
				<v-list-tile v-else @click="toggleVisible(item.name)" :key="item.text">
					<v-list-tile-action>
						<v-icon>
							{{ item.icon }}
						</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>
							{{ item.text }}
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
	</div>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
		return {
      drawerIsOpen: false,
      drawerItems: [
				// { name: 'a', icon: 'contacts', text: 'Contacts'},
        // { name: 'formSubmitter', icon: 'cloud_upload', text: 'Form Submission'},
        // { name: 'courseListing', icon: 'import_export', text: 'Export Calendar'},
        // { name: 'weeklyCalendar', icon: 'date_range', text: 'Weekly Calendar'},
        // { name: 'b', icon: 'settings', text: 'Settings'},
        // { name: 'c', icon: 'message', text: 'Messages'},
        // { name: 'd', icon: 'help', text: 'Help'}
        // { icon: 'contacts', text: 'Contacts', event: ""},
        // { icon: 'assignment', text: 'Form Submission'},
        // { icon: 'import_export', text: 'Export Calendar'},
        // { icon: 'calendar_today', text: 'Calendar'},
        // { icon: 'settings', text: 'Settings'},
        // { icon: 'message', text: 'Messages'},
				// { icon: 'help', text: 'Help'}
				{
					name: 'formSubmitter',
					icon: 'assignment',
					text: 'Forms',
					open: false,
					children: [
						{ name: 'formSubmitNewCourse', icon:'send', text: 'Submit Form' },
						{ name: 'viewCurrSuggestions', icon:'pageview', text: 'View Submissions' }
					]
				},
				{
					name: 'weeklyCalendar',
          icon: 'event',
          text: 'Calendar',
          open: false,
          children: [
            { name: 'viewFinalTimetable', icon:'calendar_view', text: 'View Calendar' },
            { name: 'exportCoursesForPlanner', icon:'save_alt', text: 'Export Calendar' },
			{ name: 'viewTimetableToSuggest', icon:'timelapse', text: 'Suggest Timings' },
			{ name: 'viewSuggestions', icon:'timelapse', text: 'View Suggestions' },
            { name: 'requestChangesToCalendar', icon:'reply_all', text: 'Request Changes' },
            { name: 'viewExistingRequests', icon:'view_array', text: 'View Requests' }
          ]
				},
				{ name: 'courseListingForViewer', icon: 'line_style', text: 'Course List'}
			]
		}
	},
	methods: {
		toggleVisible(name) {
			this.$emit('changeComp', name)
		}
	}
}
</script>