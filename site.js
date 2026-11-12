/* Project Dux homepage: motion control and the small explanatory tools.

   Every tool works without this script: the page ships a default in its HTML and the
   controls stay hidden until the script reveals them. Text is set with textContent only,
   never as HTML. Nothing typed or chosen is stored or sent anywhere. The figures in the
   "percent or points" tool are the visitor's own choices, not results from any study. */
(function () {
  'use strict';

  var byId = function (id) { return document.getElementById(id); };

  function make(tag, text, attrs) {
    var node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (attrs) Object.keys(attrs).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    return node;
  }

  function fill(parent, children) {
    while (parent.firstChild) parent.removeChild(parent.firstChild);
    children.forEach(function (child) { parent.appendChild(child); });
  }

  function listItems(lines) {
    return lines.map(function (line) { return make('li', line); });
  }

  /* ---------------------------------------------------------------- */
  /* Motion: the orbit turns only once the script runs, and can stop.  */
  /* ---------------------------------------------------------------- */
  (function () {
    var button = byId('motion');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!button || reduce) return;
    document.documentElement.classList.add('motion-on');
    button.hidden = false;
    button.addEventListener('click', function () {
      var paused = document.body.classList.toggle('paused');
      button.textContent = paused ? 'Play motion' : 'Pause motion';
    });
    var art = document.querySelector('.art');
    if (art && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        art.classList.toggle('offscreen', !entries[0].isIntersecting);
      }).observe(art);
    }
  })();

  /* ---------------------------------------------------------------- */
  /* What kind of help fits this moment? (qualitative guide)           */
  /* Drawn from library chapters 01, 03, 04, 08 and 11, and S01/S05/S06. */
  /* ---------------------------------------------------------------- */
  var FIT = {
    practise: {
      verdict: 'Make the first attempt yourself. If you get stuck, ask for a hint or a question, not the answer.',
      tryThis: ['Work the problem alone first, and mark where you got stuck.', 'Ask for one hint or one question, not a worked solution.', 'Then redo it without help, and explain each step out loud.'],
      watch: ['Practice that feels easier is not the same as learning. In one high-school maths study, open chat help raised practice scores but was followed by lower scores on a later test taken without it.', 'Feeling confident is not the same as being able to do it alone.'],
      link: ['library/03-learning-and-independence.html', 'Learning and independence →']
    },
    draft: {
      verdict: 'Keep the writing yours. Ask for questions and comments, then decide what to change.',
      tryThis: ['Ask what is unclear or unsupported, not for a rewrite.', 'Ask which claims would need a source.', 'Compare the comments with a teacher’s or a classmate’s, and choose what to act on.'],
      watch: ['A polished rewrite can sound better while saying less of what you meant.', 'Rules for AI on assignments differ by class and task. When unsure, ask.'],
      link: ['library/08-assessment.html', 'Assessment in an AI-rich setting →']
    },
    concept: {
      verdict: 'An explanation can help. Then check whether you can use it on your own.',
      tryThis: ['Ask for an explanation at your level, then for one example.', 'Explain it back in your own words, or teach it to someone.', 'Check one key claim against a textbook, a teacher, or another trusted source.'],
      watch: ['A fluent explanation can still be wrong.', 'Understanding shows when you can apply the idea to a new problem without help.'],
      link: ['library/01-ai-literacy.html', 'AI literacy →']
    },
    ideas: {
      verdict: 'Write your own ideas first, then use suggestions to stretch them, not replace them.',
      tryThis: ['List three ideas of your own before asking.', 'Ask for ideas that challenge or complicate yours.', 'Choose one, and write down why you chose it.'],
      watch: ['Choosing between ideas, and saying why, is part of the learning.', 'Whether and how to credit suggested ideas depends on the class and the task.'],
      link: ['library/11-learning-activities.html', 'Learning activities to try →']
    },
    facts: {
      verdict: 'Treat the answer as a lead to follow, not as a source.',
      tryThis: ['Find the original source the claim depends on.', 'Check who published it, and when.', 'Note where good sources disagree, and say so.'],
      watch: ['A generated answer can sound certain and still be wrong, including about where it came from.', 'Asking the same tool again is not an independent check.'],
      link: ['library/22-reading-studies.html', 'Reading claims carefully →']
    },
    child: {
      verdict: 'Explore together, with an adult close by, and check the service’s age rules first.',
      tryThis: ['Try it side by side the first time, and talk about what it says.', 'Agree when to stop, and who to tell if something feels wrong.', 'Keep names, photos, school, and home details out of the chat.'],
      watch: ['There is no universal safe age. Services set their own terms, and laws differ by place.', 'Child-rights guidance raises particular concerns about chatbots that present themselves as friends.'],
      link: ['library/04-children-and-safeguards.html', 'Children and safeguards →']
    }
  };

  (function () {
    var select = byId('fit-select');
    if (!select) return;
    var render = function () {
      var item = FIT[select.value] || FIT.practise;
      byId('fit-verdict').textContent = item.verdict;
      fill(byId('fit-try'), listItems(item.tryThis));
      fill(byId('fit-watch'), listItems(item.watch));
      var link = byId('fit-link');
      link.setAttribute('href', item.link[0]);
      link.textContent = item.link[1];
    };
    select.addEventListener('change', render);
    byId('fit-field').hidden = false;
    render(); // match any choice the browser restored
  })();

  /* ---------------------------------------------------------------- */
  /* Who does what in a learning moment (qualitative guide)            */
  /* ---------------------------------------------------------------- */
  var ROLE_LABELS = { main: 'Main role', help: 'Can help', depends: 'Depends', limited: 'Limited', unable: 'Not able to', none: 'Not their role' };
  var TASKS = ['Set the goal', 'Do the thinking', 'Give feedback', 'Judge what was learned', 'Protect personal information'];
  var ROLES = {
    learner: {
      caption: 'The learner’s part',
      summary: 'The learner does the part that builds the skill: trying, choosing, checking, and explaining. Others can support that work, but cannot do it for them.',
      rows: [['help', 'Says what they want to understand or be able to do.'], ['main', 'Makes the attempt, gets stuck, and works it through.'], ['help', 'Reviews their own work and, sometimes, a peer’s.'], ['help', 'Can explain what they understand, and where they are unsure.'], ['help', 'Chooses what to type, with guidance suited to their age.']]
    },
    teacher: {
      caption: 'An educator’s part',
      summary: 'An educator sets the purpose, decides where a tool fits, and judges learning in ways every learner can access. A tool can save some steps; the judgment stays with them.',
      rows: [['main', 'Sets learning objectives and adapts them to the learners in front of them.'], ['none', 'Can model, prompt, and question, but cannot do the learner’s thinking.'], ['main', 'Gives feedback that knows the learner, the task, and the goal.'], ['main', 'Decides how learning is shown, with accessible alternatives.'], ['main', 'Follows school rules, reviews tools, and teaches safe sharing.']]
    },
    family: {
      caption: 'A family’s part',
      summary: 'A family knows the child outside school: their sleep, mood, and what they find hard. They can explore tools together and help a child know when to stop and who to tell.',
      rows: [['help', 'Can talk about what the child is curious about and why it matters.'], ['none', 'Can encourage a first attempt, rather than doing it for them.'], ['help', 'Can ask the child to explain what they learned.'], ['depends', 'Sees changes over time that a single test may miss.'], ['main', 'Sets home rules and checks age terms, especially for young children.']]
    },
    tool: {
      caption: 'An AI tool’s part',
      summary: 'A tool can respond at any hour and offer hints, examples, and comments. It cannot know what a learner can do alone, and anything typed into it may be collected.',
      rows: [['limited', 'Can suggest, but does not know the goal unless it is told.'], ['limited', 'Can offer hints. Doing the work instead skips the practice.'], ['help', 'Gives quick comments that can be useful, generic, or wrong.'], ['unable', 'Cannot tell what someone can do without it.'], ['unable', 'Collects what is typed. Check its data terms before sharing anything personal.']]
    }
  };

  (function () {
    var field = byId('roles-field');
    if (!field) return;
    var render = function () {
      var checked = field.querySelector('input:checked');
      var role = ROLES[checked ? checked.value : 'learner'];
      byId('roles-summary').textContent = role.summary;
      byId('roles-caption').textContent = role.caption;
      fill(byId('roles-body'), role.rows.map(function (row, i) {
        var tr = make('tr');
        tr.appendChild(make('th', TASKS[i], { scope: 'row' }));
        var td = make('td');
        td.appendChild(make('span', ROLE_LABELS[row[0]], { 'class': 'role-tag', 'data-role': row[0] }));
        td.appendChild(document.createTextNode(row[1]));
        tr.appendChild(td);
        return tr;
      }));
    };
    field.addEventListener('change', render);
    field.hidden = false;
    render();
  })();

  /* ---------------------------------------------------------------- */
  /* Keep it, or hand it over? (sorting game, no score)                 */
  /* ---------------------------------------------------------------- */
  var CARDS = [
    { text: 'Write my essay about the water cycle.', lean: 'hands', note: 'A finished essay skips the part where you work out what you think and how to say it. Asking for questions about your own draft keeps that work with you.' },
    { text: 'Ask me three questions that would make my essay stronger.', lean: 'keeps', note: 'You still decide what to change and why. The questions push your thinking without replacing it.' },
    { text: 'Give me the answer to question 4.', lean: 'hands', note: 'It depends on timing. After a real attempt, checking an answer can help. Before one, it skips the practice the question was set for.' },
    { text: 'I got 12 for question 4. Where might my method have gone wrong?', lean: 'keeps', note: 'You made the attempt and you are looking for the error yourself. That is close to how a good tutor would help.' },
    { text: 'Summarise this chapter so I don’t have to read it.', lean: 'hands', note: 'A summary can be useful for review, but reading and making sense of the chapter is often the learning itself.' },
    { text: 'Quiz me on this chapter after I’ve read it.', lean: 'keeps', note: 'Recalling what you read, and finding the gaps, is active practice. Check any quiz answer you are unsure of against the chapter.' },
    { text: 'Translate this article into my first language so I can read it.', lean: 'depends', note: 'Often this is access support: it lets you reach the ideas. If the task is to practise reading in a new language, it may hand over the very skill being practised.' },
    { text: 'Show me one similar worked example, then let me try the next one alone.', lean: 'keeps', note: 'A worked example followed by your own attempt keeps the doing with you. Trying the next one alone is what shows the learning.' }
  ];
  var SORT_LABEL = { keeps: 'Keeps the thinking with me', hands: 'Hands the thinking over' };

  (function () {
    var play = byId('sort-play');
    if (!play) return;
    var index = 0;
    var choices = [];
    var card = byId('sort-card');
    var count = byId('sort-count');
    var buttons = byId('sort-buttons');
    var feedback = byId('sort-feedback');
    var feedbackText = byId('sort-feedback-text');
    var next = byId('sort-next');
    var done = byId('sort-done');

    var show = function () {
      var item = CARDS[index];
      count.textContent = 'Card ' + (index + 1) + ' of ' + CARDS.length;
      card.textContent = '“' + item.text + '”';
      buttons.hidden = false;
      feedback.hidden = true;
      done.hidden = true;
      card.hidden = false;
      count.hidden = false;
    };

    buttons.addEventListener('click', function (event) {
      var target = event.target.closest('button[data-sort]');
      if (!target) return;
      var item = CARDS[index];
      var picked = target.getAttribute('data-sort');
      choices[index] = picked;
      var lead = item.lean === 'depends'
        ? 'You sorted it as “' + SORT_LABEL[picked] + '”. This one honestly depends on the purpose. '
        : (picked === item.lean ? 'You sorted it as “' + SORT_LABEL[picked] + '”. ' : 'You sorted it as “' + SORT_LABEL[picked] + '”. Another way to see it: ');
      feedbackText.textContent = lead + item.note;
      buttons.hidden = true;
      feedback.hidden = false;
      next.textContent = index === CARDS.length - 1 ? 'See all eight' : 'Next card';
      next.focus();
    });

    next.addEventListener('click', function () {
      index += 1;
      if (index < CARDS.length) { show(); buttons.querySelector('button').focus(); return; }
      card.hidden = true;
      count.hidden = true;
      feedback.hidden = true;
      fill(byId('sort-summary'), CARDS.map(function (item, i) {
        var lean = item.lean === 'depends' ? 'depends on the purpose' : (item.lean === 'keeps' ? 'usually keeps the thinking' : 'usually hands it over');
        return make('li', '“' + item.text + '” You chose: ' + SORT_LABEL[choices[i]].toLowerCase() + '. It ' + lean + '.');
      }));
      done.hidden = false;
      byId('sort-done-title').focus();
    });

    byId('sort-again').addEventListener('click', function () {
      index = 0; choices = []; show(); buttons.querySelector('button').focus();
    });

    byId('sort-static').hidden = true;
    play.hidden = false;
    show();
  })();

  /* ---------------------------------------------------------------- */
  /* Percent or points? (illustration on visitor-chosen numbers)       */
  /* ---------------------------------------------------------------- */
  (function () {
    var base = byId('percent-base');
    var change = byId('percent-change');
    if (!base || !change) return;
    var round = function (n) { return Math.round(n * 10) / 10; };
    var fmt = function (n) { return String(round(n)).replace(/\.0$/, ''); };
    var render = function () {
      var b = Number(base.value);
      var c = Number(change.value);
      var other = b * (1 - c / 100);
      var gap = b - other;
      byId('percent-base-out').textContent = fmt(b);
      byId('percent-change-out').textContent = fmt(c) + '%';
      byId('bar-base').style.width = b + '%';
      byId('bar-other').style.width = other + '%';
      byId('bar-base-label').textContent = fmt(b);
      byId('bar-other-label').textContent = fmt(other);
      var line;
      if (c === 0) line = 'No difference: both groups average ' + fmt(b) + '. In one study, that still would not show the two approaches are the same.';
      else if (round(gap) === c) line = fmt(c) + '% lower than an average of ' + fmt(b) + ' is ' + fmt(other) + ': here the gap happens to be ' + fmt(gap) + ' points too, because the average is 100.';
      else line = fmt(c) + '% lower than an average of ' + fmt(b) + ' is ' + fmt(other) + ': a gap of ' + fmt(gap) + ' points, not ' + fmt(c) + '.';
      byId('percent-sum').textContent = line;
    };
    var timer;
    var settle = function () { clearTimeout(timer); timer = setTimeout(render, 120); };
    base.addEventListener('input', settle);
    change.addEventListener('input', settle);
    byId('percent-controls').hidden = false;
    render();
  })();

  /* ---------------------------------------------------------------- */
  /* After I used it (private check-in; nothing stored or sent)         */
  /* ---------------------------------------------------------------- */
  var NEXT_STEPS = {
    q1: 'Next time, try a first attempt before asking, even a rough one. Your attempt shows what kind of help you need.',
    q2: 'Try explaining the result out loud or in writing without looking. Where you get stuck is what to revisit.',
    q3: 'Pick one claim and check it in a textbook, with a teacher, or in an original source.',
    q4: 'Keep names, addresses, photos, and school details out of chats, and check what the service does with what you type.',
    q5: 'Ask your teacher what is allowed for this task. Rules differ between classes and assignments.',
    q6: 'If you would not want to say how you used it, that may be worth a conversation with a teacher you trust.'
  };

  (function () {
    var form = byId('checkin-form');
    if (!form) return;
    var result = byId('checkin-result');
    var answered = function () {
      return Object.keys(NEXT_STEPS).filter(function (q) { return form.querySelector('input[name="' + q + '"]:checked'); });
    };
    var render = function (focus) {
      var done = answered();
      var notYet = Object.keys(NEXT_STEPS).filter(function (q) {
        var input = form.querySelector('input[name="' + q + '"]:checked');
        return input && input.value === 'no';
      });
      var lede;
      if (!done.length) lede = 'Answer any of the questions above, then look here. You can skip any you prefer not to answer.';
      else if (!notYet.length) lede = 'You answered yes to every question you answered. That sounds like the thinking stayed with you. Keep checking in, especially on new kinds of tasks.';
      else lede = 'Each “not yet” is a place to look next, not a failure. Here are some ideas:';
      byId('checkin-result-lede').textContent = lede;
      fill(byId('checkin-result-list'), listItems(notYet.map(function (q) { return NEXT_STEPS[q]; })));
      result.hidden = false;
      if (focus) result.focus();
    };
    form.addEventListener('submit', function (event) { event.preventDefault(); render(true); });
    form.addEventListener('reset', function () { result.hidden = true; });
    byId('checkin-buttons').hidden = false;
    if (answered().length) render(false); // the browser restored answers
  })();
})();
