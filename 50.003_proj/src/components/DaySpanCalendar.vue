<template>
    <v-container fluid fill-height class="ds-calendar-container">
      <v-layout>
        <v-flex xs12>
          <v-toolbar color="white" flat>
            <v-flex xs1/>
      
            <v-layout align-center justify-center>
              <div>
                <slot name="prev" v-bind="{prev, prevLabel, calendar}">
                  <v-tooltip bottom>
                    <v-btn slot="activator"
                      icon depressed class="ds-light-forecolor ds-skinny-button"
                      @click="prev" >
                      <v-icon>keyboard_arrow_left</v-icon>
                    </v-btn>
                    <span>{{ prevLabel }}</span>
                  </v-tooltip>
                </slot>
              </div>
              
              <div>
                <slot name="summary" v-bind="{summary, calendar}">
                  <h1  class="title ds-light-forecolor" style="margin-bottom:0">
                    {{ summary }}
                  </h1>
                </slot>
              </div>
              
              <div>
                <slot name="next" v-bind="{next, nextLabel, calendar}">
                  <v-tooltip bottom>
                    <v-btn slot="activator"
                      icon depressed
                      class="ds-light-forecolor ds-skinny-button"
                      @click="next">
                      <v-icon>keyboard_arrow_right</v-icon>
                    </v-btn>
                    <span>{{ nextLabel }}</span>
                  </v-tooltip>
                </slot>
              </div>
            </v-layout>
            
            <v-flex xs1>
              <slot name="view" v-bind="{currentType, types}">
                <v-menu>
                  <v-btn flat slot="activator">
                    {{ currentType.label }}
                    <v-icon>arrow_drop_down</v-icon>
                  </v-btn>
                  <v-list>
                    <v-list-tile v-for="type in types"
                      :key="type.id"
                      @click="currentType = type">
                      <v-list-tile-content>
                        <v-list-tile-title>{{ type.label }}</v-list-tile-title>
                      </v-list-tile-content>
                    </v-list-tile>
                  </v-list>
                </v-menu>
              </slot>
            </v-flex>
          </v-toolbar>
        
          <ds-gestures
            @swipeleft="next"
            @swiperight="prev">
            
            <div v-if="currentType.schedule" class="ds-expand">
              <slot name="calendarAppAgenda" v-bind="{$scopedSlots, $listeners, calendar, add, edit, viewDay}">
                <ds-agenda
                  v-bind="{$scopedSlots}"
                  v-on="$listeners"
                  :read-only="readOnly"
                  :calendar="calendar"
                  @add="add"
                  @edit="edit"
                  @view-day="viewDay"
                ></ds-agenda>
              </slot>
            </div>

            <div v-else class="ds-expand">
              <slot name="weeklyCalendar" v-bind="{$scopedSlots, $listeners, calendar, add, addAt, edit, viewDay, handleAdd, handleMove}">
                <ds-calendar ref="calendar"
                  v-bind="{$scopedSlots}"
                  v-on="$listeners"
                  :calendar="calendar"
                  :read-only="readOnly"
                  @add="add"
                  @add-at="addAt"
                  @edit="edit"
                  @view-day="viewDay"
                  @added="handleAdd"
                  @moved="handleMove"
                ></ds-calendar>
              </slot>
            </div>
          </ds-gestures>

          <slot name="calendarAppEventDialog" v-bind="{$scopedSlots, $listeners, calendar, eventFinish}">
            <ds-event-dialog ref="eventDialog"
              v-bind="{$scopedSlots}"
              v-on="$listeners"
              :calendar="calendar"
              :read-only="readOnly || eventLocked"
              @saved="eventFinish"
              @actioned="eventFinish"
            ></ds-event-dialog>
          </slot>

          <slot name="calendarAppOptions" v-bind="{optionsVisible, optionsDialog, options, chooseOption}">
            <v-dialog ref="optionsDialog"
              v-model="optionsVisible"
              v-bind="optionsDialog"
              :fullscreen="$dayspan.fullscreenDialogs">
              <v-list>
                <template v-for="option in options">
                  <v-list-tile :key="option.text" @click="chooseOption( option )">
                    {{ option.text }}
                  </v-list-tile>
                </template>
              </v-list>
            </v-dialog>
          </slot>

          <slot name="calendarAppPrompt" v-bind="{promptVisible, promptDialog, promptQuestion, choosePrompt}">
            <v-dialog ref="promptDialog"
              v-model="promptVisible"
              v-bind="promptDialog">
              <v-card>
                <v-card-title>{{ promptQuestion }}</v-card-title>
                <v-card-actions>
                  <v-btn color="primary" flat @click="choosePrompt( true )">
                    {{ labels.promptConfirm }}
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn color="secondary" flat @click="choosePrompt( false )">
                    {{ labels.promptCancel }}
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </slot>

          <slot name="calendarAppAdd" v-bind="{allowsAddToday, addToday}">
            <v-fab-transition v-if="!readOnly">
              <v-btn
                class="ds-add-event-today"
                color="primary"
                fixed bottom right fab
                v-model="allowsAddToday"
                @click="addToday">
                <v-icon>add</v-icon>
              </v-btn>
            </v-fab-transition>
          </slot>
          <slot name="containerInside" v-bind="{events, calendar}"></slot>
         </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import { Constants, Sorts, Calendar, Day, Units, Weekday, Month, DaySpan, PatternMap, Time, Op, Schedule } from 'dayspan';
import Vuetify from 'vuetify';
import DaySpanVuetify from 'dayspan-vuetify';
	
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'dayspan-vuetify/dist/lib/dayspan-vuetify.min.css';

export default {
  name: 'dsCalendarApp',
  props:
  {
    username: {
      type: String
    },
    suggestible: {
      type: Boolean
    },
    requestable: {
      type: Boolean
    },
    events: {
      type: Array
    },
    calendar: {
      type: Calendar,
      default() {
        return Calendar.weeks();
      }
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    types:
    {
      type: Array,
      default() {
        return this.$dsDefaults().types;
      }
    },
    allowsAddToday: {
      type: Boolean,
      default() {
        return this.$dsDefaults().allowsAddToday;
      }
    },
    formats: {
      validate(x) {
        return this.$dsValidate(x, 'formats');
      },
      default() {
        return this.$dsDefaults().formats;
      }
    },
    labels: {
      validate(x) {
        return this.$dsValidate(x, 'labels');
      },
      default() {
        return this.$dsDefaults().labels;
      }
    },
    styles: {
      validate(x) {
        return this.$dsValidate(x, 'styles');
      },
      default() {
        return this.$dsDefaults().styles;
      }
    },
    optionsDialog: {
      validate(x) {
        return this.$dsValidate(x, 'optionsDialog');
      },
      default() {
        return this.$dsDefaults().optionsDialog;
      }
    },
    promptDialog: {
      validate(x) {
        return this.$dsValidate(x, 'promptDialog');
      },
      default() {
        return this.$dsDefaults().promptDialog;
      }
    }
  },
  data: vm => ({
    optionsVisible: false,
    options: [],
    promptVisible: false,
    promptQuestion: '',
    promptCallback: null,
    eventLocked: true
  }),
  watch:
  {
    'events': 'applyEvents',
    'calendar': 'applyEvents'
  },
  computed:
  {
    currentType:
    {
      get()
      {
        return this.types.find((type) =>
          type.type === this.calendar.type &&
          type.size === this.calendar.size
        ) || this.types[0];
      },
      set(type)
      {
        this.rebuild(undefined, true, type);
      }
    },
    summary()
    {
      let small = this.$vuetify.breakpoint.xs;
      if (small)
      {
        return this.calendar.start.format( this.formats.xs );
      }
      let large = this.$vuetify.breakpoint.mdAndUp;
      return this.calendar.summary(false, !large, false, !large);
    },
    todayDate()
    {
      return this.$dayspan.today.format( this.formats.today );
    },
    nextLabel()
    {
      return this.labels.next( this.currentType );
    },
    prevLabel()
    {
      return this.labels.prev( this.currentType );
    },
    toolbarStyle()
    {
      let large = this.$vuetify.breakpoint.lgAndUp;
      return large ? this.styles.toolbar.large : this.styles.toolbar.small;
    },
    hasCreatePopover()
    {
      return !!this.$scopedSlots.eventCreatePopover;
    },
    canAddDay()
    {
      return this.$dayspan.features.addDay && !this.readOnly && !this.$dayspan.readOnly;
    },
    canAddTime()
    {
      return this.$dayspan.features.addTime && !this.readOnly && !this.$dayspan.readOnly;
    }
  },
  created() {
    this.$eventHub.$on('apply-events', this.applyEvents);
    this.$eventHub.$on('view-day', this.viewDay);
  },
  mounted()
  {
    if (!this.$dayspan.promptOpen)
    {
      this.$dayspan.promptOpen = (question, callback) => {
        this.promptVisible = false;
        this.promptQuestion = question;
        this.promptCallback = callback;
        this.promptVisible = true;
      };
    }
    this.applyEvents();
  },
  beforeDestroy() {
      this.$eventHub.$off('apply-events');
      this.$eventHub.$off('view-day', this.viewDay);
  },
  methods:
  {
    setState(state)
    {
      state.eventSorter = state.listTimes
        ? Sorts.List([Sorts.FullDay, Sorts.Start])
        : Sorts.Start;
      this.calendar.set( state );
      this.triggerChange();
    },
    applyEvents()
    {
      if (this.events)
      {
        this.calendar.removeEvents();
        this.calendar.addEvents(this.events);
      }
    },
    isType(type, aroundDay)
    {
      let cal = this.calendar;
      return (cal.type === type.type && cal.size === type.size &&
          (!aroundDay || cal.span.matchesDay(aroundDay)));
    },
    rebuild (aroundDay, force, forceType)
    {
      let type = forceType || this.currentType || this.types[ 2 ];
      if (this.isType( type, aroundDay ) && !force)
      {
        return;
      }
      let input = {
        type: type.type,
        size: type.size,
        around: aroundDay,
        eventsOutside: true,
        preferToday: false,
        listTimes: type.listTimes,
        updateRows: type.updateRows,
        updateColumns: type.listTimes,
        fill: !type.listTimes,
        otherwiseFocus: type.focus,
        repeatCovers: type.repeat
      };
      this.setState( input );
    },
    next()
    {
      this.calendar.unselect().next();
      this.triggerChange();
    },
    prev()
    {
      this.calendar.unselect().prev();
      this.triggerChange();
    },
    setToday()
    {
      this.rebuild( this.$dayspan.today );
    },
    viewDay(day)
    {
      this.rebuild( day, false, this.types[ 0 ] );
    },
    edit(calendarEvent)
    {
      let eventDialog = this.$refs.eventDialog;
      eventDialog.edit(calendarEvent);
      this.eventLocked = calendarEvent.data.locked;
    },
    editPlaceholder(createEdit)
    {
      let placeholder = createEdit.calendarEvent;
      let details = createEdit.details;
      let eventDialog = this.$refs.eventDialog;
      let calendar = this.$refs.calendar;
      eventDialog.addPlaceholder( placeholder, details );
      eventDialog.$once('close', calendar.clearPlaceholder);
    },
    add(day)
    {
      if (!this.canAddDay)
      {
        return;
      }
      let eventDialog = this.$refs.eventDialog;
      let calendar = this.$refs.calendar;
      let useDialog = !this.hasCreatePopover;
      calendar.addPlaceholder( day, true, useDialog );
      if (useDialog)
      {
        //fill in suggestedBy and locked status by default for suggestible mode
        if (this.suggestible){
          eventDialog.addSchedule(day, Schedule.forDay(day), {suggestedBy:this.username, locked: false});
        } 
        else if (this.requestable){
          eventDialog.addSchedule(day, Schedule.forDay(day), {requestedBy:this.username, locked: false});
        }
        else {
          eventDialog.add(day);
        }
        eventDialog.$once('close', calendar.clearPlaceholder);
      }
    },
    addAt(dayHour)
    {
      if (!this.canAddTime)
      {
        return;
      }
      let eventDialog = this.$refs.eventDialog;
      let calendar = this.$refs.calendar;
      let useDialog = !this.hasCreatePopover;
      let at = dayHour.day.withHour( dayHour.hour );
      calendar.addPlaceholder( at, false, useDialog );
      if (useDialog)
      {
        //fill in suggestedBy and locked status by default for suggestible mode
        if (this.suggestible){
          eventDialog.addSchedule(dayHour.day, Schedule.forTime(dayHour.day, dayHour.hour), {suggestedBy:this.username, locked: false});
        } 
        else if (this.requestable){
          eventDialog.addSchedule(dayHour.day, Schedule.forTime(dayHour.day, dayHour.hour), {requestedBy:this.username, locked: false});
        } 
        else{
          eventDialog.addAt(dayHour.day, dayHour.hour);
        }
        eventDialog.$once('close', calendar.clearPlaceholder);
      }
    },
    addToday()
    {
      if (!this.canAddDay)
      {
        return;
      }
      let eventDialog = this.$refs.eventDialog;
      let calendar = this.$refs.calendar;
      let useDialog = !this.hasCreatePopover || !calendar;
      let day = this.$dayspan.today;
      if (!this.calendar.filled.matchesDay( day ))
      {
        let first = this.calendar.days[ 0 ];
        let last = this.calendar.days[ this.calendar.days.length - 1 ];
        let firstDistance = Math.abs( first.currentOffset );
        let lastDistance = Math.abs( last.currentOffset );
        day = firstDistance < lastDistance ? first: last;
      }
      calendar && calendar.addPlaceholder( day, true, useDialog );
      if (useDialog)
      {
        //fill in suggestedBy and locked status by default for suggestible mode
        if (this.suggestible){
          eventDialog.addSchedule(day, Schedule.forDay(day), {suggestedBy:this.username, locked: false});
        } 
        else if (this.requestable){
          eventDialog.addSchedule(dayHour.day, Schedule.forTime(dayHour.day, dayHour.hour), {requestedBy:this.username, locked: false});
        } 
        else {
          eventDialog.add( day );
        }
        calendar && eventDialog.$once('close', calendar.clearPlaceholder);
      }
    },
    handleAdd(addEvent)
    {
      let eventDialog = this.$refs.eventDialog;
      let calendar = this.$refs.calendar;
      addEvent.handled = true;
      if (!this.hasCreatePopover)
      {
        if (addEvent.placeholder.fullDay)
        {
          eventDialog.add(addEvent.span.start, addEvent.span.days(Op.UP));
        }
        else
        {
          eventDialog.addSpan(addEvent.span);
        }
        eventDialog.$once('close', addEvent.clearPlaceholder);
      }
      else
      {
        calendar.placeholderForCreate = true;
      }
    },
    handleMove(moveEvent)
    {
      //if suggestible and event chosen is locked, no action is taken
      //moveEvent.calendarEvent.event.data.locked
      if ((this.suggestible || this.requestable) && moveEvent.calendarEvent.event.data.locked){
        return;
      }
      let calendarEvent = moveEvent.calendarEvent;
      let target = moveEvent.target;
      let targetStart = target.start;
      let sourceStart = calendarEvent.time.start;
      let schedule = calendarEvent.schedule;
      let options = [];
      moveEvent.handled = true;
      let callbacks = {
        cancel: () => {
          moveEvent.clearPlaceholder()
        },
        single: () => {
          calendarEvent.move( targetStart );
          this.eventsRefresh();
          moveEvent.clearPlaceholder();
          this.$emit('event-update', calendarEvent.event);
        },
        instance: () => {
          calendarEvent.move( targetStart );
          this.eventsRefresh();
          moveEvent.clearPlaceholder();
          this.$emit('event-update', calendarEvent.event);
        },
        duplicate: () => {
          schedule.setExcluded( targetStart, false );
          this.eventsRefresh();
          moveEvent.clearPlaceholder();
          this.$emit('event-update', calendarEvent.event);
        },
        all: () => {
          schedule.moveTime( sourceStart.asTime(), targetStart.asTime() );
          this.eventsRefresh();
          moveEvent.clearPlaceholder();
          this.$emit('event-update', calendarEvent.event);
        }
      };
      options.push({
        text: this.labels.moveCancel,
        callback: callbacks.cancel
      });
      if (schedule.isSingleEvent())
      {
        options.push({
          text: this.labels.moveSingleEvent,
          callback: callbacks.single
        });
        if (this.$dayspan.features.moveDuplicate)
        {
          options.push({
            text: this.labels.moveDuplicate,
            callback: callbacks.duplicate
          });
        }
      }
      else
      {
        if (this.$dayspan.features.moveInstance)
        {
          options.push({
            text: this.labels.moveOccurrence,
            callback: callbacks.instance
          });
        }
        if (this.$dayspan.features.moveDuplicate)
        {
          options.push({
            text: this.labels.moveDuplicate,
            callback: callbacks.duplicate
          });
        }
        if (this.$dayspan.features.moveAll &&
            !schedule.isFullDay() &&
            targetStart.sameDay(sourceStart))
        {
          options.push({
            text: this.labels.moveAll,
            callback: callbacks.all
          });
        }
      }
      this.options = options;
      this.optionsVisible = true;
    },
    chooseOption(option)
    {
      if (option)
      {
        option.callback();
      }
      this.optionsVisible = false;
    },
    choosePrompt(yes)
    {
      this.promptCallback( yes );
      this.promptVisible = false;
    },
    eventFinish(ev)
    {
      this.triggerChange();
    },
    eventsRefresh()
    {
      this.calendar.refreshEvents();
      this.triggerChange();
    },
    triggerChange()
    {
      this.$emit('change', {
        calendar: this.calendar
      });
    }
  }
}
</script>

<style lang="scss">
.ds-skinny-button {
  margin-left: 2px !important;
  margin-right: 2px !important;
}
.ds-expand {
  width: 100%;
  height: 100%;
}
.ds-calendar-container {
  padding: 0px !important;
  position: relative;
}
.v-btn--floating.ds-add-event-today {
  .v-icon {
    width: 24px;
    height: 24px;
  }
}
</style>

