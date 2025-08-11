package v1

import (
	"context"
	"os/exec"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	v1pb "github.com/usememos/memos/proto/gen/api/v1"
)

func (s *APIV1Service) Chat(ctx context.Context, request *v1pb.ChatRequest) (*v1pb.ChatResponse, error) {
	cmd := exec.Command("bash", "-c", "source ai/venv/bin/activate && python3 ai/main.py")
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create stdin pipe: %v", err)
	}

	go func() {
		defer stdin.Close()
		stdin.Write([]byte(request.Message + "\n"))
	}()

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to run python script: %v, output: %s", err, string(output))
	}

	return &v1pb.ChatResponse{
		Response: string(output),
	}, nil
}
