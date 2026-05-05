import pytest
from src.studio_service import StudioService
from src.artist_repository import ArtistRepository
from src.studio_room_repository import StudioRoomRepository
from src.session_repository import SessionRepository
from src.waitlist_repository import WaitlistRepository


@pytest.fixture
def service():
    return StudioService(
        StudioRoomRepository(),
        ArtistRepository(),
        SessionRepository(),
        WaitlistRepository()
    )

# 1. Teste de Sucesso de reserva
 
def test_reserva_com_sucesso(service):
    resultado = service.reserve_room(10, 1) 

    assert resultado is True

# 2. Teste de Reserva de sala inexistente

def test_reserva_sala_inexistente(service):
    resultado = service.reserve_room(10, 999) # <--- Sala com id inexistente.

    assert resultado is False

# 3. Teste de artista inexistente

def test_reserva_artista_inexistente(service):
    resultado = service.reserve_room(999, 1) # <--- Artista com id inexistente.

    assert resultado is False

# 4. Teste de Assinatura nao paga.

def test_reserva_sem_assinatura(service):
    resultado = service.reserve_room(30, 1) # <--- Artista esta com o 'subscription_paid': False' ou seja nao pagou.

    assert resultado is False

# 5. Teste de artista bloqueado

def test_reserva_artista_bloqueado(service):
    resultado = service.reserve_room(20, 1) # <--- Artista esta com o 'blocked': True' ou seja esta bloqueado.

    assert resultado is False

# 6. Limite de sessoes

def test_reserva_limite_sessoes(service):
    service.reserve_room(10, 1) # <--- 1* Sessão
    service.reserve_room(10, 2) # <--- 2* Sessão

    resultado = service.reserve_room(10, 3) # <--- Deve falhar ao tentar uma 3* Sessão.

    assert resultado is False 

# 7. Entrar na fila com sucesso

def test_entrar_fila_sucesso(service):
    resultado = service.join_waitlist(10, 3) # <--- Dados corretos e validados
    assert resultado is True

# 8. Fila duplicada

def test_fila_duplicada(service):
    service.join_waitlist(10, 3)

    resultado = service.join_waitlist(10, 3) # <-- O mesmo artista fazendo a mesma chamada da fila

    assert resultado is False

# 9. Encerramento sem fila

def test_encerramento_sem_fila(service):
    service.reserve_room(10, 1)

    resultado = service.close_room_session(10, 1) # <-- Verifica que a sessão existia e foi encerrada com sucesso

    assert resultado is True

# 10. Encerramento COM fila

def test_encerramento_com_fila(service):
    service.reserve_room(10, 1) # <--- Arstista com id 10 reserva a sala
    service.join_waitlist(40, 1) # <--- Arstista com id 40 entra na fila de espera

    resultado = service.close_room_session(10, 1)

    assert resultado is True    # <-- Verifica que a sessão existia e foi encerrada com sucesso
    assert service.studio_room_repository.is_available(1) is False  # <-- Verifica que a sala não foi liberada porque ainda existe fila

# 11. Reserva remove da fila

def test_reserva_remove_da_fila(service):
    service.join_waitlist(10, 3) # <--- Entra na fila de espera

    resultado = service.reserve_room(10, 3) # <--- Remove da fila de espera e retorna true para a reserva do quarto

    assert resultado is True

# 12. Fluxo completo

def test_fluxo_completo(service):
    service.reserve_room(10, 1) # <--- Artista 10 reserva sala
    service.join_waitlist(40, 1) # <--- Artista 40 entra ma fila de espera para a mesma sala
    service.close_room_session(10, 1) # <--- Verifica que a sessão existia e foi encerrada com sucesso

    resultado = service.reserve_room(40, 1) # <--- Remove da fila de espera e retorna true para a reserva do quarto

    assert resultado is True

# 13. Não pode reservar se NÃO for o primeiro da fila

def test_reserva_nao_eh_primeiro_da_fila(service):
    service.reserve_room(10, 1)  # <-- Artista 10 ocupa a sala
    service.join_waitlist(40, 1)  # <-- Artista 40 entra na fila (1º)
    service.join_waitlist(50, 1)  # <-- Artista 50 entra na fila (2º)

    service.close_room_session(10, 1)  # <-- Encerra a sessão, sala continua ocupada por causa da fila

    resultado = service.reserve_room(50, 1)  # <-- Artista 50 tenta reservar (não é o primeiro da fila)

    assert resultado is False  # <-- Deve falhar porque só o primeiro da fila pode reservar

# 14. Primeiro da fila consegue reservar

def test_primeiro_da_fila_consegue_reservar(service):
    service.reserve_room(10, 1)  # <-- Sala ocupada pelo artista 10
    service.join_waitlist(40, 1)  # <-- Artista 40 entra na fila (1º)
    service.join_waitlist(50, 1)  # <-- Artista 50 entra na fila (2º)

    service.close_room_session(10, 1)  # <-- Encerra sessão (sala continua bloqueada pela fila)

    resultado = service.reserve_room(40, 1)  # <-- Primeiro da fila tenta reservar

    assert resultado is True  # <-- Deve conseguir reservar

# 15. Não pode entrar na fila se a sala estiver disponível

def test_nao_pode_entrar_fila_sala_disponivel(service):
    resultado = service.join_waitlist(10, 1)  # <-- Tenta entrar na fila de uma sala livre

    assert resultado is False  # <-- Deve falhar porque não faz sentido fila com sala livre