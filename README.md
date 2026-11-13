# Offline-to-Online Attribution: Measuring Web Lift from TV

A simple, practical method for answering a question every TV advertiser asks: **did that spot actually drive anyone to the website?**

I originated this approach at an agency to connect linear TV and CTV spend to website activity. The idea went to the agency's leadership for review. This repo walks through the method with made-up sample data.

## The problem

TV and other offline channels don't come with click-through data. Clients see a schedule, an invoice, and a delivery report, but not what happened online after the ad ran. Without that link, budget decisions get made on reach and cost alone.

## The approach

Every spot has a known air time, from the station's post-log. Website analytics (GA4) records sessions by the minute. Line the two up, and you can see whether traffic jumps right after a spot airs.

For each spot:

1. **Baseline:** average sessions per minute in the 10 minutes *before* the spot aired.
2. **Response window:** total sessions in the 8 minutes *after* the spot aired.
3. **Lift:** response sessions minus what the baseline would predict for the same window.

Then roll the results up by station (or daypart, market, creative) and compare **cost per lifted session**. That shows where the money is actually working.

The window lengths here are illustrative. In practice you tune them to the brand, the call to action, and how quickly response tends to show up.

## Files

| File | What it is |
|---|---|
| `spots.csv` | Sample spot schedule: air time, station, market, length, cost |
| `sessions_by_minute.csv` | Sample minute-level website sessions |
| `lift.py` | Calculates lift per spot and cost per lifted session by station |

Run it with Python 3, no extra packages needed:

```
python lift.py
```

Sample output:

```
Station     Spots    Lift     Cost  Cost/Lift
Station C       2   127.2     1240       9.75
Station A       2    74.0      900      12.16
Station B       2    15.6      600      38.46
```

In this example, Station B costs nearly four times as much per lifted session as Station C, which is a clear signal to shift budget.

## Working with imperfect data

Real data is messy, and the method has to account for it:

- **Overlapping spots:** when two spots air minutes apart, their response windows overlap. Flag those, or split the lift between them.
- **Organic trends:** traffic rises and falls through the day on its own. A short before-and-after baseline helps, and comparing against the same time on days without spots helps more.
- **Time alignment:** post-log times and analytics times must be in the same time zone and as precise as possible.
- **Small numbers:** a single spot's lift is noisy. Decisions should rest on patterns across many spots, not one.

## How the results get used

The output answers practical questions: which stations, dayparts, and markets drive real online response, and what that response costs. It pairs well with call tracking (vanity numbers or unique tracking numbers by station), which I've used to tie offline media to leads and, where the data was available, to which leads actually converted.

---

*All data in this repository is made up for demonstration. No client data is included.*
