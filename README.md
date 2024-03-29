# Toodledo Calendar Filter

## About

Filter toodledto ical with datetime.

## Usage

Subscribe this url to Calendar.app(replace url with your ical url).

Find your ical url here [iCal Subscriptions ✓ Toodledo](https://www.toodledo.com/tools/sync_ical.php),
it seems like:

```
webcal://www.toodledo.com/id/xxxxxxxxxxxxxxx/ical_live_events.ics
```

replace webcal with http, url encode the url, and put as a prama to 

```
https://toodledo-calendar-filter.alswl.com/filter_by_datetime?url=http%3A%2F%2Fwww.toodledo.com%2Fid%2Fxxxxxxxxxxxxxxx%2Fical_live_events.ics&is_fix_due_datetime=true
```

Now, subscribe the url to your Canlender.app.


Before:

![before](https://raw.githubusercontent.com/alswl/toodledo_calendar_filter/master/snapshots/before.png)

After:

![after](https://raw.githubusercontent.com/alswl/toodledo_calendar_filter/master/snapshots/after.png)


## Build

```
VERSION=$(git rev-parse --short HEAD)
dk build -t ghcr.io/alswl/toodledo_calendar_filter .
dk tag ghcr.io/alswl/toodledo_calendar_filter:latest ghcr.io/alswl/toodledo_calendar_filter:${VERSION}
dk push ghcr.io/alswl/toodledo_calendar_filter:${VERSION}
```
