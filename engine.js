// Prorata Math engine - bill arithmetic by days, in whole cents.
// Mirrored by oracle.py; keep the op order identical.
// Amounts are owner-entered; the currency is never named or converted.

function _m(x) {
  if (!isFinite(x) || x <= 0 || x > 1000000) throw new Error("bill must be between 0 and 1000000, over 0");
  return Math.floor(x * 100 + 0.5);
}

function _money(c) {
  var whole = Math.floor(c / 100), frac = c % 100;
  return whole + "." + (frac < 10 ? "0" : "") + frac;
}

function _day(n) {
  return n + (n === 1 ? " day" : " days");
}

function _days(d) {
  if (!Number.isInteger(d) || d < 1 || d > 366) throw new Error("days in period must be a whole number from 1 to 366");
  return d;
}

// The prorate truth: the part of a bill that covers the days used.
function prorateTruth(bill, days, used) {
  var c = _m(bill);
  var d = _days(days);
  if (!Number.isInteger(used) || used < 0 || used > d) throw new Error("days used must be a whole number from 0 to the days in the period");
  var share = Math.floor((2 * c * used + d) / (2 * d));
  return "A " + _money(c) + " bill over " + _day(d) + ", " + _day(used) + " used: " + _money(share) + ".";
}

// The daily truth: what one day of the bill costs.
function dailyTruth(bill, days) {
  var c = _m(bill);
  var d = _days(days);
  var r = Math.floor((200 * c + d) / (2 * d));
  var whole = Math.floor(r / 10000);
  var f = String(r % 10000);
  while (f.length < 4) f = "0" + f;
  while (f.length > 2 && f.charAt(f.length - 1) === "0") f = f.slice(0, -1);
  return "A " + _money(c) + " bill over " + _day(d) + " is " + whole + "." + f + " per day.";
}

// The split truth: one bill shared by days present, to the cent.
function splitTruth(bill, list) {
  var c = _m(bill);
  var parts = String(list).split(",").map(function (p) { return p.trim(); });
  if (parts.length < 2 || parts.length > 12) throw new Error("enter 2 to 12 day counts separated by commas");
  var ds = parts.map(function (p) {
    if (!/^[0-9]+$/.test(p) || parseInt(p, 10) > 366) throw new Error("each day count must be a whole number from 0 to 366");
    return parseInt(p, 10);
  });
  var s = ds.reduce(function (a, b) { return a + b; }, 0);
  if (s <= 0) throw new Error("day counts must add up to more than 0");
  var base = ds.map(function (d) { return Math.floor(c * d / s); });
  var rem = ds.map(function (d) { return (c * d) % s; });
  var left = c - base.reduce(function (a, b) { return a + b; }, 0);
  var order = ds.map(function (_, i) { return i; }).sort(function (a, b) { return rem[b] - rem[a] || a - b; });
  for (var k = 0; k < left; k++) base[order[k]] += 1;
  return "Bill " + _money(c) + " split over " + s + (s === 1 ? " person-day" : " person-days") + " (" + ds.join(", ") + "): " +
    base.map(_money).join(", ") + ".";
}
