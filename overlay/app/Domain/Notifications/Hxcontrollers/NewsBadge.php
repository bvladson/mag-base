<?php

namespace Leantime\Domain\Notifications\Hxcontrollers;

use Leantime\Core\Controller\HtmxController;

/**
 * MAG: removido da base — contador de novidades do blog leantime.io.
 *
 * A classe continua existindo porque o classmap otimizado do Composer a referencia
 * (apagar o arquivo faria a rota responder 500). Sem métodos get/post/run, o
 * Frontcontroller não encontra método válido e qualquer acesso responde 404.
 */
class NewsBadge extends HtmxController
{
    protected static string $view = 'notifications::partials.newsBadge';
}
