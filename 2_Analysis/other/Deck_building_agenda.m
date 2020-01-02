clear

Num_step = 4;
Num_card_step = [40, 45, 50, 55];
Min_agenda_step = [18, 20, 22, 24];

Deck_size = 40:80;

for n=Deck_size
    if (n<Num_card_step(2))
        Min_agenda(n-40+1) = Min_agenda_step(1);
    elseif (n<Num_card_step(3))
        Min_agenda(n-40+1) = Min_agenda_step(2);
    elseif (n<Num_card_step(4))
        Min_agenda(n-40+1) = Min_agenda_step(3);
    else
        floor((n-50)./5)
        Min_agenda(n-40+1) = Min_agenda_step(3) + 2*floor((n-50)./5);
    end
end

Agenda_deck_ratio = Min_agenda/2./Deck_size;
Agenda_deck_ratio_min = (Min_agenda/3)./Deck_size;

yyaxis left
stairs(Deck_size, Min_agenda)
xlabel('Deck size');
ylabel('Min Agenda points in Deck')
yyaxis right
stairs(Deck_size, Agenda_deck_ratio)
ylabel('Ratio');
hold on
stairs(Deck_size, Agenda_deck_ratio_min)