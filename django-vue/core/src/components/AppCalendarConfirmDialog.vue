<template>
	<v-dialog
		v-model="dialog"
		max-width="290"
	>
		<v-card>
			<slot name="title"></slot>
			<slot name="text"></slot>
			<v-card-actions>
				<v-spacer></v-spacer>
				<slot name="noButton"></slot>
				<slot name="yesButton"></slot>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
  export default {
		name: 'AppCalendarEventDialog',
		props: {
			dialog: {
				type: Boolean
			}
		}
  }
</script>