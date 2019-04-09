Vue.component("push-list", {
  props: ["item"],
  template: `<tr>
		<td>{{ item.first_name }} {{ item.last_name }}</td>
		<td>{{ item.subject_code }} {{ item.subject_name }}</td>
		<td>{{ item.cohort_size }} x {{ item.cohort_num }}</td>
		<td><a class="btn btn-info" href="" role="button">Edit</a></td>
	</tr>
	`
});

Vue.component("error-boundary", {
  data: () => ({
    error: false
  }),
  errorCaptured(err, vm, info) {
    this.error = true;
  },
  render(h) {
    return this.error ? h("p", "errorCaptured") : this.$slots.default[0];
  }
});

Vue.component("course-table", {
  props: ["values"],
  template: `
  <table class="table table-hover">
    <thead class="thead-dark">
        <tr>
            <th scope='col'>Name</th>
            <th scope='col'>Subject</th>
            <th scope='col'>Cohort Size x No. of Cohorts</th>
            <th scope='col'>Edit</th>
        </tr>
    </thead>
    <error-boundary v-for="entry in values">
        <push-list
        key="entry.pk"
        v-bind:item="entry.fields">
        </push-list>
    </error-boundary>
  </table>`
});

var app = new Vue({
  el: "#populated-list",
  data: {
    values: tables,
    headervalues: {
      e1: "Name",
      e2: "Subject",
      e3: "Cohort Size x No. of Cohorts",
      e4: "Edit"
    }
  }
});
