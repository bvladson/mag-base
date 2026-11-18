@if ($login::userIsAtLeast($roles::$editor))
    <div class="btn-group pull-left" style="margin-right:5px;">
        <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown"><?=$tpl->__("links.new_with_icon") ?> <span class="caret"></span></button>
        <ul class="dropdown-menu">
            <li><a href="#/tickets/newTicket">Adicionar tarefa</a></li>
            <li><a href="#/tickets/editMilestone">Adicionar marco</a></li>

        </ul>
    </div>
@endif

