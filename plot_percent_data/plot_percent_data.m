%uiimport('nounData_allText.csv')
%save('novel_data.mat','ALL_NOUNS_IN_ALL_WORDS','FILENAME','PRONOUNS_IN_ALL_WORDS','PROPER_NOUNS_IN_ALL_NOUNS','PROPER_NOUNS_IN_ALL_WORDS','REGULAR_NOUNS_IN_ALL_NOUNS','TEXT_SIZE');

clear all
close all
clc

load('novel_data.mat')

% Trim first column
ALL_NOUNS_IN_ALL_WORDS = ALL_NOUNS_IN_ALL_WORDS(2:end);
FILENAME = FILENAME(2:end);
PRONOUNS_IN_ALL_WORDS = PRONOUNS_IN_ALL_WORDS(2:end);
PROPER_NOUNS_IN_ALL_NOUNS = PROPER_NOUNS_IN_ALL_NOUNS(2:end);
PROPER_NOUNS_IN_ALL_WORDS = PROPER_NOUNS_IN_ALL_WORDS(2:end);
REGULAR_NOUNS_IN_ALL_NOUNS = REGULAR_NOUNS_IN_ALL_NOUNS(2:end);
TEXT_SIZE = TEXT_SIZE(2:end);

% (1) ALL NOUNS / TOTAL WORDS
pfit1 = polyfit(log(TEXT_SIZE), log(ALL_NOUNS_IN_ALL_WORDS), 1);
yfit1 = polyval(pfit1, log(TEXT_SIZE));
f1 = figure(1);
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
plot(log(TEXT_SIZE),log(ALL_NOUNS_IN_ALL_WORDS),'o','MarkerFaceColor','g','Color','g','MarkerSize',12)
xlabel('Log(# Words)')
ylabel('Log(# Nouns)') 
title(['[# Nouns] \sim [# Words]^{' num2str(pfit1(1)) '}'])
hold on;
plot(log(TEXT_SIZE),yfit1,'-k')
hold off;


% (2) PRONOUNS / TOTAL WORDS
pfit2 = polyfit(log(TEXT_SIZE), log(PRONOUNS_IN_ALL_WORDS), 1);
yfit2 = polyval(pfit2, log(TEXT_SIZE));
f2 = figure(2);
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
plot(log(TEXT_SIZE),log(PRONOUNS_IN_ALL_WORDS),'o','MarkerFaceColor','r','Color','r','MarkerSize',12)
xlabel('Log(# Words)')
ylabel('Log(# Pronouns)') 
title(['[# Pronouns] \sim [# Words]^{' num2str(pfit2(1)) '}'])
hold on;
plot(log(TEXT_SIZE),yfit2,'-k')
hold off;

 
% (3) PROPER NOUNS / ALL NOUNS
pfit3 = polyfit(log(ALL_NOUNS_IN_ALL_WORDS), log(PROPER_NOUNS_IN_ALL_NOUNS), 1);
yfit3 = polyval(pfit3, log(ALL_NOUNS_IN_ALL_WORDS));
f3 = figure(3);
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
plot(log(ALL_NOUNS_IN_ALL_WORDS),log(PROPER_NOUNS_IN_ALL_NOUNS),'o','MarkerFaceColor','b','Color','b','MarkerSize',12)
xlabel('Log(# Nouns)')
ylabel('Log(# Proper Nouns)') 
title(['[# Proper Nouns] \sim [# Nouns]^{' num2str(pfit3(1)) '}'])
hold on;
plot(log(ALL_NOUNS_IN_ALL_WORDS),yfit3,'-k')
hold off;

% (4) REGULAR NOUNS / ALL NOUNS
pfit4 = polyfit(log(ALL_NOUNS_IN_ALL_WORDS), log(REGULAR_NOUNS_IN_ALL_NOUNS), 1);
yfit4 = polyval(pfit4, log(ALL_NOUNS_IN_ALL_WORDS));
f4 = figure(4);
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
plot(log(ALL_NOUNS_IN_ALL_WORDS),log(REGULAR_NOUNS_IN_ALL_NOUNS),'o','MarkerFaceColor','m','Color','m','MarkerSize',12)
xlabel('Log(# Nouns)')
ylabel('Log(# Regular Nouns)') 
title(['[# Regular Nouns] \sim [# Nouns]^{' num2str(pfit4(1)) '}'])
hold on;
plot(log(ALL_NOUNS_IN_ALL_WORDS),yfit4,'-k')
hold off;
ylim([-1 0])

% printing to files
print(f1,'-dpng','-r200','ALL NOUNS_TEXT_SIZE.jpg')
print(f2,'-dpng','-r200','ALL PRONOUNS_TEXT_SIZE.jpg')
print(f3,'-dpng','-r200','PROPER_NOUNS_ALL NOUNS.jpg')
print(f4,'-dpng','-r200','REGULAR_NOUNS_ALL NOUNS.jpg')